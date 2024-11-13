-- First set the database character set
ALTER DATABASE lokabhasha CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Update existing tables
ALTER TABLE Languages CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE Modules CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE Questions CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Before running any queries, set the connection character set
SET NAMES utf8mb4;

-- Clear existing data
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE Questions;
TRUNCATE TABLE Modules;
TRUNCATE TABLE Languages;
SET FOREIGN_KEY_CHECKS = 1;

-- Insert Languages
INSERT INTO Languages (name) VALUES 
('hi'),
('kn'),
('ta');

-- Insert Modules for each language
INSERT INTO Modules (lang_id, name, `desc`) 
SELECT lang_id, 'easy', 'Basic phrases and questions'
FROM Languages;

INSERT INTO Modules (lang_id, name, `desc`)
SELECT lang_id, 'medium', 'Intermediate phrases and questions'
FROM Languages;

-- Insert Questions for Hindi (lang_id = 1)
INSERT INTO Questions (m_id, question, exp_ans, category)
-- Easy Module Hindi
SELECT m.m_id, 'What time is it?', 'अभी कितने बजे हैं?', 'Q'
FROM Modules m WHERE m.lang_id = 1 AND m.name = 'easy'
UNION ALL
SELECT m.m_id, 'When can we meet?', 'हम कब मिल सकते हैं?', 'Q'
FROM Modules m WHERE m.lang_id = 1 AND m.name = 'easy'
UNION ALL
SELECT m.m_id, 'It is a beautiful day.', 'यह एक सुंदर दिन है।', 'Statement'
FROM Modules m WHERE m.lang_id = 1 AND m.name = 'easy'

-- Medium Module Hindi
UNION ALL
SELECT m.m_id, 'How much does it cost?', 'इसकी कीमत क्या है?', 'Q'
FROM Modules m WHERE m.lang_id = 1 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'I am going to a movie tomorrow.', 'मैं कल फिल्म देखने जा रहा हूं।', 'Statement'
FROM Modules m WHERE m.lang_id = 1 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'It was raining in the morning.', 'सुबह बारिश हो रही थी।', 'Statement'
FROM Modules m WHERE m.lang_id = 1 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'My grandparents live in Bangalore.', 'मेरे दादा-दादी बैंगलोर में रहते हैं।', 'Statement'
FROM Modules m WHERE m.lang_id = 1 AND m.name = 'medium';

-- Insert Questions for Kannada (lang_id = 2)
INSERT INTO Questions (m_id, question, exp_ans, category)
-- Easy Module Kannada
SELECT m.m_id, 'What time is it?', 'ಈಗ ಎಷ್ಟು ಗಂಟೆ?', 'Q'
FROM Modules m WHERE m.lang_id = 2 AND m.name = 'easy'
UNION ALL
SELECT m.m_id, 'When can we meet?', 'ನಾವು ಯಾವಾಗ ಸಿಗಬಹುದು?', 'Q'
FROM Modules m WHERE m.lang_id = 2 AND m.name = 'easy'
UNION ALL
SELECT m.m_id, 'It is a beautiful day.', 'ಇದು ಒಂದು ಸುಂದರವಾದ ದಿನ.', 'Statement'
FROM Modules m WHERE m.lang_id = 2 AND m.name = 'easy'

-- Medium Module Kannada
UNION ALL
SELECT m.m_id, 'How much does it cost?', 'ಇದು ಎಷ್ಟು ಬೆಲೆ?', 'Q'
FROM Modules m WHERE m.lang_id = 2 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'I am going to a movie tomorrow.', 'ನಾನು ನಾಳೆ ಸಿನಿಮಾಗೆ ಹೋಗುತ್ತಿದ್ದೇನೆ.', 'Statement'
FROM Modules m WHERE m.lang_id = 2 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'It was raining in the morning.', 'ಬೆಳಗ್ಗೆ ಮಳೆ ಬರುತ್ತಿತ್ತು.', 'Statement'
FROM Modules m WHERE m.lang_id = 2 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'My grandparents live in Bangalore.', 'ನನ್ನ ಅಜ್ಜ-ಅಜ್ಜಿ ಬೆಂಗಳೂರಿನಲ್ಲಿ ವಾಸಿಸುತ್ತಾರೆ.', 'Statement'
FROM Modules m WHERE m.lang_id = 2 AND m.name = 'medium';

-- Insert Questions for Tamil (lang_id = 3)
INSERT INTO Questions (m_id, question, exp_ans, category)
-- Easy Module Tamil
SELECT m.m_id, 'What time is it?', 'இப்போது என்ன நேரம்?', 'Q'
FROM Modules m WHERE m.lang_id = 3 AND m.name = 'easy'
UNION ALL
SELECT m.m_id, 'When can we meet?', 'நாம் எப்போது சந்திக்கலாம்?', 'Q'
FROM Modules m WHERE m.lang_id = 3 AND m.name = 'easy'
UNION ALL
SELECT m.m_id, 'It is a beautiful day.', 'இது ஒரு அழகான நாள்.', 'Statement'
FROM Modules m WHERE m.lang_id = 3 AND m.name = 'easy'

-- Medium Module Tamil
UNION ALL
SELECT m.m_id, 'How much does it cost?', 'இது எவ்வளவு விலை?', 'Q'
FROM Modules m WHERE m.lang_id = 3 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'I am going to a movie tomorrow.', 'நான் நாளை திரைப்படம் பார்க்க போகிறேன்.', 'Statement'
FROM Modules m WHERE m.lang_id = 3 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'It was raining in the morning.', 'காலையில் மழை பெய்தது.', 'Statement'
FROM Modules m WHERE m.lang_id = 3 AND m.name = 'medium'
UNION ALL
SELECT m.m_id, 'My grandparents live in Bangalore.', 'என் தாத்தா பாட்டி பெங்களூரில் வசிக்கிறார்கள்.', 'Statement'
FROM Modules m WHERE m.lang_id = 3 AND m.name = 'medium';