CREATE TABLE Client_info (
  client_id INT NOT NULL,
  ClientFullName VARCHAR(255),
  ClientPhoneNumber VARCHAR(255),
  ClientEmail VARCHAR(255),
  ClientTgUsername VARCHAR(255),
  PRIMARY KEY (client_id)
);

CREATE TABLE Doctor_info (
  doctor_id INT NOT NULL,
  DoctorFullName VARCHAR(255),
  DoctorInfo VARCHAR(255),
  Photo VARCHAR(255),
  PRIMARY KEY (doctor_id)
);

CREATE TABLE Service_type (
  id INT AUTO_INCREMENT,
  ServiceType VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE Service_info (
  id INT AUTO_INCREMENT,
  ServiceType_fk INT,
  ServiceName VARCHAR(255),
  ServicePrice INT,
  PRIMARY KEY (id),
  FOREIGN KEY (ServiceType_fk) REFERENCES Service_type(id)
);

CREATE TABLE Doctor_service (
  id INT AUTO_INCREMENT,
  service_fk INT,
  doctor_fk INT,
  PRIMARY KEY (id),
  FOREIGN KEY (service_fk) REFERENCES Service_info(id),
  FOREIGN KEY (doctor_fk) REFERENCES Doctor_info(doctor_id)
);

CREATE TABLE Sales_info (
  id INT AUTO_INCREMENT,
  SaleName VARCHAR(255),
  SaleDescription VARCHAR(255),
  SaleStartDate DATETIME,
  SaleEndDate DATETIME,
  PRIMARY KEY (id)
);

CREATE TABLE Coupon (
  id INT AUTO_INCREMENT,
  CouponName VARCHAR(255),
  CouponDescription VARCHAR(255),
  CouponOwner_fk INT,
  CouponStartDate DATETIME,
  CouponEndDate DATETIME,
  PRIMARY KEY (id),
  FOREIGN KEY (CouponOwner_fk) REFERENCES Client_info(client_id)
);

CREATE TABLE Statistic (
  OrderNumber BIGINT AUTO_INCREMENT,
  client_fk INT,
  service_fk INT,
  doctor_fk INT,
  DateOfApplication DATETIME,
  Coupon INT,
  Status VARCHAR(255),
  DateOfReceipt DATETIME,
  ProblemDescription VARCHAR(255),
  PRIMARY KEY (OrderNumber),
  FOREIGN KEY (client_fk) REFERENCES Client_info(client_id),
  FOREIGN KEY (service_fk) REFERENCES Service_info(id),
  FOREIGN KEY (doctor_fk) REFERENCES Doctor_info(doctor_id)
);