INSERT INTO `building` (`bid`, `bname`, `bprefix`) VALUES (2, 'Informatics Building', 'IF'), (3, 'BUUIC', 'BUUIC');

INSERT INTO `floor` (`fid`, `fname`, `bid`) VALUES (NULL, '1', '2'), (NULL, '2', '2'), (NULL, '3', '2'), 
	(NULL, '4', '2'), (NULL, '5', '2'), (NULL, '6', '2'), (NULL, '7', '2'), (NULL, '8', '2'), (NULL, '9', '2'), (NULL, '10', '2'), (NULL, '11', '2'), (NULL, '12', '2');

INSERT INTO `floor` (`fid`, `fname`, `bid`) VALUES (NULL, '1', '3'), (NULL, '2', '3'), (NULL, '3', '3'), (NULL, '4', '3'), (NULL, '5', '3'), (NULL, '6', '3');

INSERT INTO `room` (`rid`, `rname`, `fid`) VALUES (NULL, 'IF-1C01', '2'),(NULL, 'IF-1C02', '2');
INSERT INTO `room` (`rid`, `rname`, `fid`) VALUES (NULL, 'IF-2C01', '3'),(NULL, 'IF-2C02', '3'),(NULL, 'IF-2C03', '3');
INSERT INTO `room` (`rid`, `rname`, `fid`) VALUES (NULL, 'IF-3C01', '4'),(NULL, 'IF-3C02', '4'),(NULL, 'IF-3C03', '4'),(NULL, 'IF-3C04', '4'),(NULL, 'IF-3C05', '4'),(NULL, 'IF-3C06', '4');
INSERT INTO `room` (`rid`, `rname`, `fid`) VALUES (NULL, 'IF-4C01', '5'),(NULL, 'IF-4C02', '5'),(NULL, 'IF-4C03', '5'),(NULL, 'IF-4C04', '5'),(NULL, 'IF-4C05', '5'),(NULL, 'IF-4C06', '5');

INSERT INTO `room` (`rid`, `rname`, `fid`) VALUES (NULL, 'BUUIC-1-1', '14'),(NULL, 'BUUIC-1-2', '14'),(NULL, 'BUUIC-1-3', '14'),(NULL, 'BUUIC-1-3', '15');
INSERT INTO `room` (`rid`, `rname`, `fid`) VALUES (NULL, 'BUUIC-2-1', '15'),(NULL, 'BUUIC-2-2', '15'),(NULL, 'BUUIC-2-3', '15');

INSERT INTO `board` (`boid`, `bomac`, `register`, `rid`) VALUES (NULL, '7B-D3-A3-2B-20-30', '0', '12'), (NULL, 'AA-BB-CC-DD-EE-FF', '0', '12'), (NULL, '1C-87-63-7F-9C-2B', '0', '13'), (NULL, 'DE-17-D0-F2-73-43', '0', '14'), (NULL, '13-1F-03-14-B7-C5', '0', '15');

INSERT INTO `type` (`tid`, `tname`) VALUES (NULL, 'Light'), (NULL, 'Electricity'), (NULL, 'Air Conditioner'), (NULL, 'Motion');

INSERT INTO `user` (`id`, `username`, `email`, `password`, `create_time`, `is_active`) VALUES (NULL, 'admin', 'admin@mail.com', '$pbkdf2-sha256$29000$JmSsdY5R6t07h1AqpVQKwQ$Y.g5BF0EgSKCjK47wfBa45EFlIALaxD8k0snzPvxRBM', CURRENT_TIMESTAMP, 1);

INSERT INTO `sensor` (`sid`, `sname`, `tid`, `boid`) VALUES (NULL, 'Light 1', '1', '1'), (NULL, 'Light 2', '1', '1'), (NULL, 'Elec 1', '2', '1'), (NULL, 'Air 1', '3', '1'), (NULL, 'Light x', '1', '3'), (NULL, 'Light y', '1', '3'), (NULL, 'Light z', '1', '3'), (NULL, 'Light a', '1', '4'), (NULL, 'Elec b', '2', '4'), (NULL, 'Air c', '3', '4');




