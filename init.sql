SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS test324
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE test324;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'user',
    otp_secret VARCHAR(32) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CHECK (email LIKE '%@hvbma.or.th'),
    CHECK (role IN ('user', 'admin', 'dev'))
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

INSERT INTO users (email, password, role, otp_secret) 
VALUES ('dev@hvbma.or.th', '1', 'dev', 'HIRVZ5VCQP655R5RWNUX3FY4WP3I3ZTM'),
('user@hvbma.or.th', '1', 'user', '26CHFTL7NFF2BVAPNVCDCGIKTTT3X6QG'),
('admin@hvbma.or.th', '1', 'admin', 'DT7QEYOIUXDZOGAWX77UZOGNIUFDU5TK');

CREATE TABLE IF NOT EXISTS volunteers (
    volunteer_id BIGINT(11) PRIMARY KEY,
    prefix VARCHAR(10) NOT NULL,       
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    birth_date DATE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    community VARCHAR(255) NOT NULL,
    service VARCHAR(255) NOT NULL,
    sub_district VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- ข้อมูลส่วนตัว
    volunteer_id BIGINT(11) NOT NULL,
    prefix VARCHAR(10) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    community VARCHAR(255) NOT NULL,

    -- ข้อมูลพื้นที่
    sub_district VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,

    -- ข้อมูลเดือนและปีที่ปฏิบัติงาน
    operation_month VARCHAR(20) NOT NULL,
    operation_year INT NOT NULL,

    -- กลุ่มกิจกรรม: ป้องกันและควบคุมโรค
    q1_prevention1_times INT NOT NULL,
    q1_prevention1_people INT NOT NULL,
    q1_prevention2_times INT NOT NULL,
    q1_prevention3_times INT NOT NULL,
    q1_prevention4_times INT NOT NULL,
    q1_prevention4_people INT NOT NULL,
    q1_prevention5_times INT NOT NULL,

    -- กลุ่มกิจกรรม: รักษาพยาบาลเบื้องต้น
    q2_treatment1_times INT NOT NULL,
    q2_treatment1_people INT NOT NULL,
    q2_treatment2_times INT NOT NULL,
    q2_treatment3_times INT NOT NULL,
    q2_treatment3_people INT NOT NULL,
    q2_treatment4_times INT NOT NULL,
    q2_treatment4_people INT NOT NULL,
    q2_treatment5_times INT NOT NULL,

    -- กลุ่มกิจกรรม: ติดตามดูแล
    q3_assistance_times INT NOT NULL,
    q3_assistance_people INT NOT NULL,

    -- กลุ่มกิจกรรม: การมีส่วนร่วม
    q4_engaging1_times INT NOT NULL,
    q4_engaging2_times INT NOT NULL,

    -- กลุ่มกิจกรรม: การให้คำปรึกษา
    q5_consult_times INT NOT NULL,
    q5_consult_people INT NOT NULL,

    -- กลุ่มกิจกรรม: งานอื่นๆ
    q6_others TEXT,

    -- หมายเหตุ
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;