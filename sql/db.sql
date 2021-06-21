-- ----------------------------
-- View structure for v_exceededviolation
-- ----------------------------
DROP VIEW IF EXISTS `v_exceededviolation`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_exceededviolation` AS select `violation`.`id` AS `id`,`violation`.`date` AS `date`,`violation`.`location` AS `location`,`violation`.`type` AS `type`,`violation`.`deadline` AS `deadline`,`violation`.`fine` AS `fine`,`vehicle`.`plate_number` AS `plate_number`,`violation`.`driver_id` AS `driver_id`,`driver`.`name` AS `driver_name`,`owner`.`identity` AS `owner_id`,`owner`.`name` AS `owner_name`,`violation`.`is_processed` AS `is_processed` from (((`trafficman_violation` `violation` join `trafficman_vehicle` `vehicle`) join `trafficman_userprofile` `driver`) join `trafficman_userprofile` `owner`) where ((`violation`.`vehicle_id` = `vehicle`.`engine_id`) and (`violation`.`driver_id` = `driver`.`identity`) and (`vehicle`.`owner_id` = `owner`.`identity`) and (curdate() > `violation`.`deadline`) and (exists(select 1 from `trafficman_violationprocess` where (`violation`.`id` = `trafficman_violationprocess`.`violation_id`)) is false or ((select `trafficman_violationprocess`.`process_time` from `trafficman_violationprocess` where (`trafficman_violationprocess`.`violation_id` = `violation`.`id`)) > `violation`.`deadline`)));

-- ----------------------------
-- View structure for v_unprocessedviolation
-- ----------------------------
DROP VIEW IF EXISTS `v_unprocessedviolation`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_unprocessedviolation` AS select `trafficman_violation`.`id` AS `id`,`trafficman_violation`.`date` AS `date`,`trafficman_violation`.`area` AS `area`,`trafficman_violation`.`type` AS `type`,`trafficman_violation`.`deadline` AS `deadline`,`trafficman_violation`.`fine` AS `fine`,`trafficman_vehicle`.`plate_number` AS `plate_number`,`trafficman_violation`.`driver_id` AS `driver_id`,`driver`.`name` AS `driver_name`,`own`.`identity` AS `owner_id`,`own`.`name` AS `owner_name`,`trafficman_violation`.`is_processed` AS `is_processed` from (((`trafficman_violation` join `trafficman_vehicle`) join `trafficman_userprofile` `driver`) join `trafficman_userprofile` `own`) where ((`trafficman_violation`.`is_processed` = 0) and (`trafficman_violation`.`driver_id` = `driver`.`identity`) and (`trafficman_violation`.`vehicle_id` = `trafficman_vehicle`.`engine_id`) and (`trafficman_vehicle`.`owner_id` = `own`.`identity`));

-- ----------------------------
-- View structure for v_vehicleowner
-- ----------------------------
DROP VIEW IF EXISTS `v_vehicleowner`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_vehicleowner` AS select `trafficman_userprofile`.`identity` AS `identity`,`trafficman_userprofile`.`name` AS `name`,`trafficman_userprofile`.`gender` AS `gender`,`trafficman_userprofile`.`ethnicity` AS `ethnicity`,`trafficman_userprofile`.`nationality` AS `nationality`,`trafficman_userprofile`.`address` AS `address`,`trafficman_userprofile`.`telephone` AS `telephone`,`trafficman_userprofile`.`mobile` AS `mobile`,`trafficman_userprofile`.`birth` AS `birth`,`trafficman_vehicle`.`engine_id` AS `engine_id`,`trafficman_vehicle`.`brand` AS `brand`,`trafficman_vehicle`.`manufacture_model` AS `manufacture_model`,`trafficman_vehicle`.`color` AS `color`,`trafficman_vehicle`.`vehicle_type` AS `vehicle_type`,`trafficman_vehicle`.`displacement` AS `displacement`,`trafficman_vehicle`.`manufacture_date` AS `manufacture_date`,`trafficman_vehicle`.`life_duration` AS `life_duration`,`trafficman_vehicle`.`plate_number` AS `plate_number`,`trafficman_vehicle`.`status` AS `status` from (`trafficman_userprofile` join `trafficman_vehicle`) where (`trafficman_userprofile`.`identity` = `trafficman_vehicle`.`owner_id`);

-- ----------------------------
-- View structure for v_violationprocessrecord
-- ----------------------------
DROP VIEW IF EXISTS `v_violationprocessrecord`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_violationprocessrecord` AS select `v`.`id` AS `id`,`v`.`date` AS `date`,`v`.`type` AS `type`,`v`.`area` AS `area`,`v`.`location` AS `location`,`v`.`point_minus` AS `point_minus`,`v`.`fine` AS `fine`,`v`.`deadline` AS `deadline`,`v`.`is_processed` AS `is_processed`,`v`.`driver_id` AS `driver_id`,`vh`.`plate_number` AS `plate_number`,`vp`.`process_time` AS `process_time` from ((`trafficman_violation` `v` join `trafficman_violationprocess` `vp`) join `trafficman_vehicle` `vh`) where ((`v`.`id` = `vp`.`violation_id`) and (`v`.`vehicle_id` = `vh`.`engine_id`));

-- ----------------------------
-- Procedure structure for p_SetDriverLicenseStatus
-- ----------------------------
DROP PROCEDURE IF EXISTS `p_SetDriverLicenseStatus`;
delimiter ;;
CREATE PROCEDURE `user002db`.`p_SetDriverLicenseStatus`()
BEGIN
  UPDATE TrafficMan_driverlicense
	SET status='F'
	WHERE TIMESTAMPDIFF(YEAR,begin_date,CURDATE())>=valid_duration+1 AND status<>'F';
	
	UPDATE TrafficMan_driverlicense
	SET points=12
	WHERE MONTH(begin_date)=MONTH(CURDATE()) AND DAY(begin_date)=DAY(CURDATE()) AND status='A';
END
;;
delimiter ;

-- ----------------------------
-- Event structure for Schedule_SetDriverLicenseStatus
-- ----------------------------
DROP EVENT IF EXISTS `Schedule_SetDriverLicenseStatus`;
delimiter ;;
CREATE EVENT `user002db`.`Schedule_SetDriverLicenseStatus`
ON SCHEDULE
EVERY '1' DAY STARTS '2021-05-26 06:15:00'
DO call p_SetDriverLicenseStatus
;
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table trafficman_education
-- ----------------------------
DROP TRIGGER IF EXISTS `t_educationUpdateTrigger`;
delimiter ;;
CREATE TRIGGER `t_educationUpdateTrigger` AFTER UPDATE ON `trafficman_education` FOR EACH ROW BEGIN
	DECLARE record_count INT;
	SELECT count(*) INTO record_count
	FROM TrafficMan_educationrecord
	WHERE TrafficMan_educationrecord.education_id = NEW.id;

	IF NEW.is_finished=1 AND record_count=0 THEN
		INSERT INTO TrafficMan_educationrecord
		VALUES (NOW(), NEW.id);

		UPDATE TrafficMan_driverlicense
		SET status='A'
		WHERE TrafficMan_driverlicense.user_profile_id=NEW.driver_id AND TrafficMan_driverlicense.status='B';
		UPDATE TrafficMan_driverlicense
		SET points=12
		WHERE TrafficMan_driverlicense.user_profile_id=NEW.driver_id;
	END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table trafficman_vehicle
-- ----------------------------
DROP TRIGGER IF EXISTS `t_closeVehicleTrigger`;
delimiter ;;
CREATE TRIGGER `t_closeVehicleTrigger` BEFORE UPDATE ON `trafficman_vehicle` FOR EACH ROW BEGIN
	IF NEW.status='E' OR NEW.status='M' THEN
		SET NEW.plate_number=null;
	END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table trafficman_violation
-- ----------------------------
DROP TRIGGER IF EXISTS `t_violationUpdateTrigger`;
delimiter ;;
CREATE TRIGGER `t_violationUpdateTrigger` AFTER UPDATE ON `trafficman_violation` FOR EACH ROW BEGIN
	DECLARE process_count INT;
	SELECT count(*) INTO process_count
	FROM TrafficMan_violationprocess
	WHERE TrafficMan_violationprocess.violation_id=NEW.id;

	IF process_count=0 THEN
		IF NEW.is_processed=1 THEN
			INSERT INTO TrafficMan_violationprocess
			VALUES (NOW(),NEW.id);
			UPDATE TrafficMan_driverlicense
			SET status='A'
			WHERE TrafficMan_driverlicense.user_profile_id=NEW.driver_id AND TrafficMan_driverlicense.status='H';
			UPDATE TrafficMan_vehicle
			SET status='A'
			WHERE TrafficMan_vehicle.engine_id=NEW.vehicle_id AND TrafficMan_vehicle.status='G';
		END IF;
	END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table trafficman_violation
-- ----------------------------
DROP TRIGGER IF EXISTS `t_violationInsertTrigger`;
delimiter ;;
CREATE TRIGGER `t_violationInsertTrigger` AFTER INSERT ON `trafficman_violation` FOR EACH ROW BEGIN
	DECLARE d_points INT;
	SELECT points INTO d_points
	FROM TrafficMan_driverlicense
	WHERE TrafficMan_driverlicense.user_profile_id = NEW.driver_id;

	IF CAST(d_points AS SIGNED)-CAST(NEW.point_minus AS SIGNED)<=0 THEN
		UPDATE TrafficMan_driverlicense
		SET points=0, status='B'
		WHERE TrafficMan_driverlicense.user_profile_id = NEW.driver_id;
		
		INSERT INTO TrafficMan_education(create_time, is_finished, driver_id)
		VALUES(NOW(), 0, NEW.driver_id);

		IF NEW.is_processed = 0 THEN
			UPDATE TrafficMan_vehicle
			SET status = 'G'
			WHERE TrafficMan_vehicle.engine_id=NEW.vehicle_id;
		ELSE
			INSERT INTO TrafficMan_violationprocess
			VALUES (NOW(),NEW.id);
		END IF;
	ELSE
		UPDATE TrafficMan_driverlicense
		SET points=d_points-NEW.point_minus
		WHERE TrafficMan_driverlicense.user_profile_id = NEW.driver_id;

		IF NEW.is_processed=0 THEN
			UPDATE TrafficMan_vehicle
			SET status = 'G'
			WHERE TrafficMan_vehicle.engine_id=NEW.vehicle_id;
			UPDATE TrafficMan_driverlicense
			SET status='H'
			WHERE TrafficMan_driverlicense.user_profile_id = NEW.driver_id;
		ELSE
			INSERT INTO TrafficMan_violationprocess
			VALUES (NOW(),NEW.id);
		END IF;
	END IF;
END
;;
delimiter ;