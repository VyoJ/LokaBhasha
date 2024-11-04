CREATE DATABASE lokabhasha;

USE lokabhasha;

-- Create Users table
CREATE TABLE Users (
    u_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    joined_on DATETIME NOT NULL,
    pref_lang INT
);

-- Create Languages table
CREATE TABLE Languages (
    lang_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Add foreign key constraint to Users table
ALTER TABLE Users
ADD CONSTRAINT fk_user_lang
FOREIGN KEY (pref_lang) REFERENCES Languages(lang_id);

-- Create APIs table
CREATE TABLE APIs (
    api INT PRIMARY KEY AUTO_INCREMENT,
    lang_id INT NOT NULL,
    FOREIGN KEY (lang_id) REFERENCES Languages(lang_id)
);

-- Create Modules table
CREATE TABLE Modules (
    m_id INT PRIMARY KEY AUTO_INCREMENT,
    lang_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    `desc` TEXT,
    pre_id INT,
    FOREIGN KEY (lang_id) REFERENCES Languages(lang_id),
    FOREIGN KEY (pre_id) REFERENCES Modules(m_id)
);

-- Create Questions table
CREATE TABLE Questions (
    q_id INT PRIMARY KEY AUTO_INCREMENT,
    m_id INT NOT NULL,
    question TEXT NOT NULL,
    exp_ans TEXT,
    category VARCHAR(50),
    FOREIGN KEY (m_id) REFERENCES Modules(m_id)
);

-- Create Answers table
CREATE TABLE Answers (
    q_id INT,
    resp_id INT,
    u_id INT,
    PRIMARY KEY (q_id, resp_id),
    FOREIGN KEY (q_id) REFERENCES Questions(q_id),
    FOREIGN KEY (u_id) REFERENCES Users(u_id)
);

-- Create Responses table
CREATE TABLE Responses (
    resp_id INT PRIMARY KEY AUTO_INCREMENT,
    response_asr TEXT,
    response_url VARCHAR(255),
    response_translate TEXT,
    latency FLOAT
);

-- Add foreign key constraint to Answers table
ALTER TABLE Answers
ADD CONSTRAINT fk_answer_response
FOREIGN KEY (resp_id) REFERENCES Responses(resp_id);

-- Create Resources table
CREATE TABLE Resources (
    lang_id INT,
    resource_id INT,
    url VARCHAR(255) NOT NULL,
    type VARCHAR(50),
    format VARCHAR(50),
    PRIMARY KEY (lang_id, resource_id),
    FOREIGN KEY (lang_id) REFERENCES Languages(lang_id)
);