-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema blocked_cars
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `blocked_cars` ;

-- -----------------------------------------------------
-- Schema blocked_cars
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `blocked_cars` DEFAULT CHARACTER SET utf8mb3 ;
USE `blocked_cars` ;

-- -----------------------------------------------------
-- Table `blocked_cars`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `blocked_cars`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `phone_number` VARCHAR(45) NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `blocked_cars`.`cars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `blocked_cars`.`cars` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `plates` VARCHAR(45) NOT NULL,
  `distance` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_cars_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_cars_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `blocked_cars`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 34
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `blocked_cars`.`joins`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `blocked_cars`.`joins` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `car_id` INT NOT NULL,
  `car_id2` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_joins_cars1_idx` (`car_id` ASC) VISIBLE,
  INDEX `fk_joins_cars3_idx` (`car_id2` ASC) VISIBLE,
  INDEX `fk_joins_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_joins_cars1`
    FOREIGN KEY (`car_id`)
    REFERENCES `blocked_cars`.`cars` (`id`),
  CONSTRAINT `fk_joins_cars3`
    FOREIGN KEY (`car_id2`)
    REFERENCES `blocked_cars`.`cars` (`id`),
  CONSTRAINT `fk_joins_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `blocked_cars`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 62
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
