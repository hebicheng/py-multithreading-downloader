-- --------------------------------------------------------
-- 主机:                           10.10.41.22
-- 服务器版本:                        5.5.60-MariaDB - MariaDB Server
-- 服务器操作系统:                      Linux
-- HeidiSQL 版本:                  9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 phonedetect_service_emulator 的数据库结构
CREATE DATABASE IF NOT EXISTS `phonedetect_service_emulator` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `phonedetect_service_emulator`;

-- 导出  表 phonedetect_service_emulator.sp_random_download_task_multiVer_copy 结构
CREATE TABLE IF NOT EXISTS `sp_random_download_task_multiVer_copy` (
  `dl_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `dl_flag` int(11) NOT NULL DEFAULT '0',
  `task_id` int(11) DEFAULT '0',
  `dl_url` varchar(1024) DEFAULT NULL,
  `dl_url_hash` varchar(32) DEFAULT NULL,
  `referer_url` varchar(256) DEFAULT NULL,
  `file_size` bigint(20) unsigned NOT NULL DEFAULT '0',
  `receive_size` bigint(20) unsigned NOT NULL DEFAULT '0',
  `begin_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `dl_status` int(11) NOT NULL DEFAULT '0' COMMENT '0：未下载，1：正在下载，2：下载成功，4：下载失败，文件不全，8：下载超时，16：下载链接拒绝访问，32：下载链接不存在，64：下载链接被重定向，128：链接为空，1024：未知错误，2048：APK大小超过限制',
  `fullpath` varchar(256) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `file_md5` varchar(32) DEFAULT NULL,
  `dl_count` double DEFAULT '0',
  `fetch_flag` int(11) DEFAULT '0' COMMENT '0:等待解析，1：正在解析，2：解析成功，3：解析失败',
  `fetch_thread` int(11) DEFAULT NULL COMMENT '鍙栬蛋鐨勭嚎绋媔d',
  `ready` bit(1) DEFAULT b'0',
  `app_category` varchar(128) DEFAULT NULL,
  `app_name` varchar(128) DEFAULT NULL,
  `app_pkg` varchar(256) DEFAULT NULL,
  `app_version` varchar(128) DEFAULT NULL,
  `app_size` float DEFAULT '0',
  `dup_type` varchar(45) DEFAULT NULL,
  `dup_id` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`dl_id`)
) ENGINE=MyISAM AUTO_INCREMENT=912224 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
