INSERT INTO `user` (`id`, `username`, `email`, `password`, `create_time`, `is_active`) VALUES (NULL, 'admin', 'admin@mail.com', '$pbkdf2-sha256$29000$JmSsdY5R6t07h1AqpVQKwQ$Y.g5BF0EgSKCjK47wfBa45EFlIALaxD8k0snzPvxRBM', CURRENT_TIMESTAMP, 1);

INSERT INTO `logs` (`lid`, `message`, `create_time`) VALUES ('1', 'first log', '2020-01-01 00:00:00')

INSERT INTO `notify` (`nid`, `ntoken`, `ntime`, `nlast_time`, `user_id`) VALUES (NULL, 'sample', '0', CURRENT_TIMESTAMP, '1');




