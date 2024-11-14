USE lokabhasha;

-- Trigger to create answer entry after response insertion
DELIMITER //
CREATE TRIGGER after_response_insert 
AFTER INSERT ON Responses
FOR EACH ROW
BEGIN
    -- Get the latest question_id for this user (assuming this is stored in a session variable)
    -- and create the answer entry
    IF @current_user_id IS NOT NULL AND @current_question_id IS NOT NULL THEN
        INSERT INTO Answers (q_id, resp_id, u_id)
        VALUES (@current_question_id, NEW.resp_id, @current_user_id);
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetNextQuestionId(
    IN p_user_id INT,
    IN p_module_id INT,
    OUT next_question_id INT
)
BEGIN
    -- Get the first question in the module that the user hasn't answered yet
    SELECT MIN(q.q_id) INTO next_question_id
    FROM Questions q
    WHERE q.m_id = p_module_id
    AND q.q_id NOT IN (
        SELECT DISTINCT a.q_id 
        FROM Answers a 
        WHERE a.u_id = p_user_id
    );
    
    -- If all questions are answered, return NULL
    IF next_question_id IS NULL THEN
        SELECT MIN(q.q_id) INTO next_question_id
        FROM Questions q
        WHERE q.m_id = p_module_id;
    END IF;
END //

DELIMITER ;

-- Helper procedure to set current user and question context
DELIMITER //
CREATE PROCEDURE SetUserContext(
    IN p_user_id INT,
    IN p_question_id INT
)
BEGIN
    SET @current_user_id = p_user_id;
    SET @current_question_id = p_question_id;
END //
DELIMITER ;

-- Example usage of setting context before inserting response
-- CALL SetUserContext(1, 1);
-- INSERT INTO Responses (response_asr, response_url, response_translate, latency) 
-- VALUES ('response text', 'url', 'translated text', 100);


DELIMITER //

-- Get response count for a specific date
CREATE FUNCTION GetDailyResponseCount(target_date DATE) 
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE response_count INT;
    SELECT COUNT(*) INTO response_count
    FROM Responses 
    WHERE DATE(created_at) = target_date;
    RETURN COALESCE(response_count, 0);
END //

-- Get most active language name
CREATE FUNCTION GetMostActiveLanguage() 
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE active_lang VARCHAR(50);
    SELECT l.name INTO active_lang
    FROM Languages l
    JOIN Modules m ON l.lang_id = m.lang_id
    JOIN Questions q ON m.m_id = q.m_id
    JOIN Answers a ON q.q_id = a.q_id
    JOIN Responses r ON a.resp_id = r.resp_id
    GROUP BY l.lang_id, l.name
    ORDER BY COUNT(r.resp_id) DESC
    LIMIT 1;
    RETURN COALESCE(active_lang, 'No active language');
END //

-- Get response count for most active language
CREATE FUNCTION GetMostActiveLanguageCount() 
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE response_count INT;
    SELECT COUNT(r.resp_id) INTO response_count
    FROM Languages l
    JOIN Modules m ON l.lang_id = m.lang_id
    JOIN Questions q ON m.m_id = q.m_id
    JOIN Answers a ON q.q_id = a.q_id
    JOIN Responses r ON a.resp_id = r.resp_id
    WHERE l.name = (
        SELECT l2.name
        FROM Languages l2
        JOIN Modules m2 ON l2.lang_id = m2.lang_id
        JOIN Questions q2 ON m2.m_id = q2.m_id
        JOIN Answers a2 ON q2.q_id = a2.q_id
        JOIN Responses r2 ON a2.resp_id = r2.resp_id
        GROUP BY l2.lang_id, l2.name
        ORDER BY COUNT(r2.resp_id) DESC
        LIMIT 1
    );
    RETURN COALESCE(response_count, 0);
END //

-- Get today's signup count
CREATE FUNCTION GetTodaySignups() 
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE signup_count INT;
    SELECT COUNT(*) INTO signup_count
    FROM Users
    WHERE DATE(joined_on) = CURDATE();
    RETURN COALESCE(signup_count, 0);
END //

-- Get overall average latency
CREATE FUNCTION GetOverallAverageLatency() 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE avg_latency DECIMAL(10,2);
    SELECT AVG(latency) INTO avg_latency
    FROM Responses;
    RETURN COALESCE(avg_latency, 0.00);
END //

-- Get language specific average latency
CREATE FUNCTION GetLanguageAverageLatency(lang_name VARCHAR(50)) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE lang_avg_latency DECIMAL(10,2);
    SELECT AVG(r.latency) INTO lang_avg_latency
    FROM Languages l
    JOIN Modules m ON l.lang_id = m.lang_id
    JOIN Questions q ON m.m_id = q.m_id
    JOIN Answers a ON q.q_id = a.q_id
    JOIN Responses r ON a.resp_id = r.resp_id
    WHERE l.name = lang_name;
    RETURN COALESCE(lang_avg_latency, 0.00);
END //

DELIMITER ;

-- Example usage:
/*
SELECT GetDailyResponseCount(CURDATE()) as today_responses;
SELECT GetMostActiveLanguage() as most_active_language;
SELECT GetMostActiveLanguageCount() as active_language_responses;
SELECT GetTodaySignups() as new_users;
SELECT GetOverallAverageLatency() as overall_latency;
SELECT GetLanguageAverageLatency('hi') as hindi_latency;
*/

DELIMITER //

CREATE FUNCTION GetUserDailyAnalytics(user_id INT, target_date DATE) 
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
    DECLARE total_count INT;
    DECLARE correct_count INT;
    DECLARE wrong_count INT;
    
    -- Get total responses
    SELECT COUNT(DISTINCT r.resp_id) INTO total_count
    FROM Responses r
    JOIN Answers a ON r.resp_id = a.resp_id
    WHERE a.u_id = user_id 
    AND DATE(r.created_at) = target_date;
    
    -- Get correct responses with collation fix
    SELECT COUNT(DISTINCT r.resp_id) INTO correct_count
    FROM Responses r
    JOIN Answers a ON r.resp_id = a.resp_id
    JOIN Questions q ON a.q_id = q.q_id
    WHERE a.u_id = user_id 
    AND DATE(r.created_at) = target_date
    AND LOWER(TRIM(r.response_translate)) COLLATE utf8mb4_unicode_ci = 
        LOWER(TRIM(q.exp_ans)) COLLATE utf8mb4_unicode_ci;
    
    -- Calculate wrong responses
    SET wrong_count = total_count - correct_count;
    
    RETURN CONCAT(
        'Total: ', total_count,
        ', Correct: ', correct_count,
        ', Wrong: ', wrong_count
    );
END //

DELIMITER ;

-- Example usage:
-- SELECT GetUserDailyAnalytics(1, CURDATE()) AS user_performance;