-- --------------------------------------------------------
-- Servidor:                     10.4.1.171
-- Versão do servidor:           5.7.33 - MySQL Community Server (GPL)
-- OS do Servidor:               Linux
-- HeidiSQL Versão:              11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para contadores
CREATE DATABASE IF NOT EXISTS `contadores` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `contadores`;

-- Copiando estrutura para tabela contadores.counters
CREATE TABLE IF NOT EXISTS `counters` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `printer_id` int(10) unsigned NOT NULL,
  `total_prints` int(11) DEFAULT NULL,
  `total_copies` int(11) DEFAULT NULL,
  `total_prints_color` int(11) DEFAULT NULL,
  `total_copies_color` int(11) DEFAULT NULL,
  `total_scans` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_counters_printers` (`printer_id`),
  CONSTRAINT `FK_counters_printers` FOREIGN KEY (`printer_id`) REFERENCES `printers` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela contadores.failures
CREATE TABLE IF NOT EXISTS `failures` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `printer_id` int(10) unsigned DEFAULT NULL,
  `failure_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_printer_failure` (`printer_id`),
  CONSTRAINT `FK_printer_failure` FOREIGN KEY (`printer_id`) REFERENCES `printers` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela contadores.printers
CREATE TABLE IF NOT EXISTS `printers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sn` varchar(10) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `type` ENUM('M','C') NOT NULL COLLATE 'latin1_swedish_ci',
  PRIMARY KEY (`id`),
  UNIQUE KEY `sn` (`sn`),
  UNIQUE KEY `ip` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Exportação de dados foi desmarcado.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
