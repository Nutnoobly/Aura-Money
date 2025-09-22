
CREATE TABLE `track` (
  `track_id` int(11) NOT NULL,
  `type` varchar(100) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `total` float DEFAULT NULL,
  `balance` float DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `user` (`user_id`, `username`, `password`, `email`) VALUES
(7, 'tester2', '$2b$12$v77ghDLdxxkemYkwoJ9oM.3fbj2urc6a98V3YiJdomo5KRtpSNd5G', 'no12@gmail.com'),
(8, 'hrz', '$2b$12$75ess50mmthFSKIHyjs4o.TsTX9to5NHAvPk6bYqq0GaOmbTy7bju', 'hrz@gmail.com');

ALTER TABLE `track`
  ADD PRIMARY KEY (`track_id`),
  ADD KEY `user_id` (`user_id`);

ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

ALTER TABLE `track`
  ADD CONSTRAINT `track_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);
COMMIT;

