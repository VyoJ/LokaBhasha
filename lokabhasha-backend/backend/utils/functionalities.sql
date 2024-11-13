-- triggers_and_procedures.sql

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

-- Procedure to check student completion status
DELIMITER //
CREATE PROCEDURE GetUserProgress(IN p_user_id INT)
BEGIN
    -- Declare variables
    DECLARE total_questions INT;
    DECLARE answered_questions INT;
    
    -- Get progress for each module
    SELECT 
        m.lang_id,
        l.name AS language_name,
        m.name AS module_name,
        COUNT(DISTINCT q.q_id) AS total_questions,
        COUNT(DISTINCT a.q_id) AS answered_questions,
        CASE 
            WHEN COUNT(DISTINCT a.q_id) = COUNT(DISTINCT q.q_id) THEN 'Completed'
            WHEN COUNT(DISTINCT a.q_id) > 0 THEN 'In Progress'
            ELSE 'Not Started'
        END AS module_status,
        ROUND((COUNT(DISTINCT a.q_id) / COUNT(DISTINCT q.q_id)) * 100, 2) AS completion_percentage
    FROM 
        Modules m
        JOIN Languages l ON m.lang_id = l.lang_id
        LEFT JOIN Questions q ON m.m_id = q.m_id
        LEFT JOIN Answers a ON q.q_id = a.q_id AND a.u_id = p_user_id
    GROUP BY 
        m.m_id, m.lang_id, l.name, m.name
    ORDER BY 
        l.name, m.name;
        
    -- Get overall progress
    SELECT 
        COUNT(DISTINCT q.q_id) AS total_questions,
        COUNT(DISTINCT a.q_id) AS completed_questions,
        ROUND((COUNT(DISTINCT a.q_id) / COUNT(DISTINCT q.q_id)) * 100, 2) AS overall_completion_percentage
    FROM 
        Questions q
        LEFT JOIN Answers a ON q.q_id = a.q_id AND a.u_id = p_user_id;
END //
DELIMITER ;

-- Example usage of the procedure
-- CALL GetUserProgress(1);

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