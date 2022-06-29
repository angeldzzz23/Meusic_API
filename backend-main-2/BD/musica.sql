-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 27-03-2022 a las 06:14:09
-- Versión del servidor: 5.7.26
-- Versión de PHP: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `musica`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=65 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add genero_musical', 7, 'add_genero_musical'),
(26, 'Can change genero_musical', 7, 'change_genero_musical'),
(27, 'Can delete genero_musical', 7, 'delete_genero_musical'),
(28, 'Can view genero_musical', 7, 'view_genero_musical'),
(29, 'Can add genero', 8, 'add_genero'),
(30, 'Can change genero', 8, 'change_genero'),
(31, 'Can delete genero', 8, 'delete_genero'),
(32, 'Can view genero', 8, 'view_genero'),
(33, 'Can add usuario_artista', 9, 'add_usuario_artista'),
(34, 'Can change usuario_artista', 9, 'change_usuario_artista'),
(35, 'Can delete usuario_artista', 9, 'delete_usuario_artista'),
(36, 'Can view usuario_artista', 9, 'view_usuario_artista'),
(37, 'Can add usuario_habilidad', 10, 'add_usuario_habilidad'),
(38, 'Can change usuario_habilidad', 10, 'change_usuario_habilidad'),
(39, 'Can delete usuario_habilidad', 10, 'delete_usuario_habilidad'),
(40, 'Can view usuario_habilidad', 10, 'view_usuario_habilidad'),
(41, 'Can add usuarios', 11, 'add_usuarios'),
(42, 'Can change usuarios', 11, 'change_usuarios'),
(43, 'Can delete usuarios', 11, 'delete_usuarios'),
(44, 'Can view usuarios', 11, 'view_usuarios'),
(45, 'Can add usuario_genero_musical', 12, 'add_usuario_genero_musical'),
(46, 'Can change usuario_genero_musical', 12, 'change_usuario_genero_musical'),
(47, 'Can delete usuario_genero_musical', 12, 'delete_usuario_genero_musical'),
(48, 'Can view usuario_genero_musical', 12, 'view_usuario_genero_musical'),
(49, 'Can add habilidad', 13, 'add_habilidad'),
(50, 'Can change habilidad', 13, 'change_habilidad'),
(51, 'Can delete habilidad', 13, 'delete_habilidad'),
(52, 'Can view habilidad', 13, 'view_habilidad'),
(53, 'Can add plataforma', 14, 'add_plataforma'),
(54, 'Can change plataforma', 14, 'change_plataforma'),
(55, 'Can delete plataforma', 14, 'delete_plataforma'),
(56, 'Can view plataforma', 14, 'view_plataforma'),
(57, 'Can add plataforma_usuario', 15, 'add_plataforma_usuario'),
(58, 'Can change plataforma_usuario', 15, 'change_plataforma_usuario'),
(59, 'Can delete plataforma_usuario', 15, 'delete_plataforma_usuario'),
(60, 'Can view plataforma_usuario', 15, 'view_plataforma_usuario'),
(61, 'Can add usuario_plataforma', 15, 'add_usuario_plataforma'),
(62, 'Can change usuario_plataforma', 15, 'change_usuario_plataforma'),
(63, 'Can delete usuario_plataforma', 15, 'delete_usuario_plataforma'),
(64, 'Can view usuario_plataforma', 15, 'view_usuario_plataforma');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'api', 'genero_musical'),
(8, 'api', 'genero'),
(9, 'api', 'usuario_artista'),
(10, 'api', 'usuario_habilidad'),
(11, 'api', 'usuarios'),
(12, 'api', 'usuario_genero_musical'),
(13, 'api', 'habilidad'),
(14, 'api', 'plataforma'),
(15, 'api', 'usuario_plataforma');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2022-03-27 00:18:10.785813'),
(2, 'auth', '0001_initial', '2022-03-27 00:18:11.777029'),
(3, 'admin', '0001_initial', '2022-03-27 00:18:12.069443'),
(4, 'admin', '0002_logentry_remove_auto_add', '2022-03-27 00:18:12.122446'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2022-03-27 00:18:12.165448'),
(6, 'contenttypes', '0002_remove_content_type_name', '2022-03-27 00:18:12.347458'),
(7, 'auth', '0002_alter_permission_name_max_length', '2022-03-27 00:18:12.423463'),
(8, 'auth', '0003_alter_user_email_max_length', '2022-03-27 00:18:12.536469'),
(9, 'auth', '0004_alter_user_username_opts', '2022-03-27 00:18:12.585472'),
(10, 'auth', '0005_alter_user_last_login_null', '2022-03-27 00:18:12.656476'),
(11, 'auth', '0006_require_contenttypes_0002', '2022-03-27 00:18:12.668477'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2022-03-27 00:18:12.723480'),
(13, 'auth', '0008_alter_user_username_max_length', '2022-03-27 00:18:12.836486'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2022-03-27 00:18:12.904490'),
(15, 'auth', '0010_alter_group_name_max_length', '2022-03-27 00:18:12.962494'),
(16, 'auth', '0011_update_proxy_permissions', '2022-03-27 00:18:13.013497'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2022-03-27 00:18:13.080500'),
(18, 'sessions', '0001_initial', '2022-03-27 00:18:13.136504'),
(19, 'api', '0001_initial', '2022-03-27 00:18:46.936761'),
(20, 'api', '0002_auto_20220326_2144', '2022-03-27 03:44:10.041577'),
(21, 'api', '0003_plataforma_usuario', '2022-03-27 03:51:04.309350'),
(22, 'api', '0004_auto_20220326_2153', '2022-03-27 03:53:50.869781'),
(23, 'api', '0005_alter_usuario_plataforma_table', '2022-03-27 03:55:17.007567'),
(24, 'api', '0006_remove_usuario_plataforma_plataforma_descripcion', '2022-03-27 04:25:49.545700');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `genero`
--

DROP TABLE IF EXISTS `genero`;
CREATE TABLE IF NOT EXISTS `genero` (
  `genero_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `genero_descripcion` varchar(200) NOT NULL,
  PRIMARY KEY (`genero_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `genero`
--

INSERT INTO `genero` (`genero_id`, `genero_descripcion`) VALUES
(1, 'Hombre'),
(2, 'Mujer');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `genero_musical`
--

DROP TABLE IF EXISTS `genero_musical`;
CREATE TABLE IF NOT EXISTS `genero_musical` (
  `genero_musical_id` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`genero_musical_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `genero_musical`
--

INSERT INTO `genero_musical` (`genero_musical_id`) VALUES
(1),
(2),
(3),
(4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habilidad`
--

DROP TABLE IF EXISTS `habilidad`;
CREATE TABLE IF NOT EXISTS `habilidad` (
  `habilidad_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `habilidad_descripcion` varchar(200) NOT NULL,
  PRIMARY KEY (`habilidad_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `habilidad`
--

INSERT INTO `habilidad` (`habilidad_id`, `habilidad_descripcion`) VALUES
(1, 'Cantar'),
(2, 'Bailar');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plataforma`
--

DROP TABLE IF EXISTS `plataforma`;
CREATE TABLE IF NOT EXISTS `plataforma` (
  `plataforma_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `plataforma_descripcion` varchar(200) NOT NULL,
  PRIMARY KEY (`plataforma_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `plataforma`
--

INSERT INTO `plataforma` (`plataforma_id`, `plataforma_descripcion`) VALUES
(1, 'Vimeo'),
(2, 'You Tube');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `usuario_id` char(32) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `correo_electronico` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `contrasena` varchar(250) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `acerca_de_mi` varchar(250) NOT NULL,
  `genero_id` bigint(20) NOT NULL,
  PRIMARY KEY (`usuario_id`),
  KEY `usuarios_genero_id_2bd9930f_fk_Genero_genero_id` (`genero_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`usuario_id`, `nombre`, `apellidos`, `fecha_nacimiento`, `correo_electronico`, `username`, `contrasena`, `fecha_creacion`, `acerca_de_mi`, `genero_id`) VALUES
('7d28686bd92548abae9a6acbb26f1955', 'GERARDO', 'SANCHEZ', '2022-10-10', 'Y1', 'CASTIGADOR', 'contrasena', '2022-03-26', 'acerca_de_mi', 1),
('fbb37b8b331a44219354a6f3bc09c461', 'GERARDOs', 'SANCHEZ', '2022-10-10', 'Ys111', 'CASTIGADORs11', 'contrasena', '2022-03-26', 'mensajes', 1),
('e98184ba2db14532ab5a9e8d860e3e3a', 'GERARDO', 'SANCHEZ', '2022-10-10', 'correo_electronico211111', 'CASTIGADOR111', 'contrasena', '2022-03-26', 'acerca_de_mi', 1),
('efa7cea0800c4f1c9db1695c494bdd57', 'GERARDOs', 'SANCHEZ', '2022-10-10', 'Ys1', 'CASTIGADORs', 'contrasena', '2022-03-26', 'acerca_de_mi', 1),
('89bfefdff60d47c782e883e1abe5d04a', 'GERARDOs', 'SANCHEZ', '2022-10-10', 'Ys11', 'CASTIGADORs1', 'contrasena', '2022-03-26', 'acerca_de_mi', 1),
('953208fea28643e8aa7a52fbe8a6c237', 'GERARDOs', 'SANCHEZ', '2022-10-10', 'Ys111', 'CASTIGADORs11', 'contrasena', '2022-03-26', 'acerca_de_mi', 1),
('df3e0ac36fc84208ad09d19f8731dbdd', 'Yorbin', 'Nuñez Martinez', '2022-10-10', 'yorbin.nunez@gmail.com', 'yorbin.nunez', 'contrasena', '2022-03-26', 'acerca_de_mi', 1),
('e8179e6f2a2946568759f08fdc1645ed', 'Yorbin', 'Nuñez Martinez', '2022-10-10', 'yorbin.nune@gmail.com', 'yorbin.nunezs', 'contrasena', '2022-03-26', 'acerca_de_mi', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_artista`
--

DROP TABLE IF EXISTS `usuario_artista`;
CREATE TABLE IF NOT EXISTS `usuario_artista` (
  `usuario_artista_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `artista_id` varchar(100) NOT NULL,
  `usuario_id` char(32) NOT NULL,
  PRIMARY KEY (`usuario_artista_id`),
  KEY `usuario_artista_usuario_id_5a18d411` (`usuario_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `usuario_artista`
--

INSERT INTO `usuario_artista` (`usuario_artista_id`, `artista_id`, `usuario_id`) VALUES
(1, '42137b8b331a44219354a6f3bc091231', 'fbb37b8b331a44219354a6f3bc09c461'),
(2, 'b8b331a44219354a6f3bc091231', 'fbb37b8b331a44219354a6f3bc09c461'),
(3, 'b8b331a44219354a6f3bc091232', 'fbb37b8b331a44219354a6f3bc09c461'),
(4, 'b8b331a44219354a6f3bc091236', 'fbb37b8b331a44219354a6f3bc09c461'),
(5, 'b8b331a44219354a6f3bc091212', 'fbb37b8b331a44219354a6f3bc09c461');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_genero_musical`
--

DROP TABLE IF EXISTS `usuario_genero_musical`;
CREATE TABLE IF NOT EXISTS `usuario_genero_musical` (
  `usuario_genero_musical_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `genero_musical_id` bigint(20) NOT NULL,
  `usuario_id` char(32) NOT NULL,
  PRIMARY KEY (`usuario_genero_musical_id`),
  KEY `usuario_genero_musical_genero_musical_id_e0dd2974` (`genero_musical_id`),
  KEY `usuario_genero_musical_usuario_id_084c225b` (`usuario_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_habilidad`
--

DROP TABLE IF EXISTS `usuario_habilidad`;
CREATE TABLE IF NOT EXISTS `usuario_habilidad` (
  `usuario_habilidad_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `habilidad_id` bigint(20) NOT NULL,
  `usuario_id` char(32) NOT NULL,
  PRIMARY KEY (`usuario_habilidad_id`),
  KEY `Usuario_habilidad_habilidad_id_689ca6a6` (`habilidad_id`),
  KEY `Usuario_habilidad_usuario_id_4a24c6cd` (`usuario_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_plataforma`
--

DROP TABLE IF EXISTS `usuario_plataforma`;
CREATE TABLE IF NOT EXISTS `usuario_plataforma` (
  `plataforma_usuario_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `url` varchar(200) NOT NULL,
  `plataforma_id` bigint(20) NOT NULL,
  `usuario_id` char(32) NOT NULL,
  PRIMARY KEY (`plataforma_usuario_id`),
  KEY `plataforma_usuario_plataforma_id_5e59b511` (`plataforma_id`),
  KEY `plataforma_usuario_usuario_id_08201fe0` (`usuario_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `usuario_plataforma`
--

INSERT INTO `usuario_plataforma` (`plataforma_usuario_id`, `url`, `plataforma_id`, `usuario_id`) VALUES
(2, 'https://www.youtube.com/watch?v=FmA8gUGAvUQ', 2, 'fbb37b8b331a44219354a6f3bc09c461'),
(3, 'https://www.youtube.com/watch?v=FmA8gUGAvU6', 2, 'fbb37b8b331a44219354a6f3bc09c461');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
