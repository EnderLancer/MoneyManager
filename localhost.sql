-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Время создания: Май 17 2020 г., 12:16
-- Версия сервера: 10.3.16-MariaDB
-- Версия PHP: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `id12652518_wallet_manager`
--
CREATE DATABASE IF NOT EXISTS `id12652518_wallet_manager` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `id12652518_wallet_manager`;

-- --------------------------------------------------------

--
-- Структура таблицы `access_lvl`
--

CREATE TABLE `access_lvl` (
  `access_level_id` int(10) UNSIGNED NOT NULL,
  `access_level_name` char(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `access_lvl`
--

INSERT INTO `access_lvl` (`access_level_id`, `access_level_name`) VALUES
(1, 'Owner'),
(2, 'Editor'),
(3, 'Updater'),
(4, 'Reader');

-- --------------------------------------------------------

--
-- Структура таблицы `action`
--

CREATE TABLE `action` (
  `action_id` int(10) UNSIGNED NOT NULL,
  `action_name` char(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `action`
--

INSERT INTO `action` (`action_id`, `action_name`) VALUES
(1, 'Earned'),
(2, 'Spent');

-- --------------------------------------------------------

--
-- Структура таблицы `currency`
--

CREATE TABLE `currency` (
  `currency_id` int(10) UNSIGNED NOT NULL,
  `currency_name` char(50) NOT NULL,
  `currency_symbol` char(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `currency`
--

INSERT INTO `currency` (`currency_id`, `currency_name`, `currency_symbol`) VALUES
(1, 'United States dollar', 'USD'),
(2, 'Ukrainian hryvnia', 'UAH');

-- --------------------------------------------------------

--
-- Структура таблицы `records`
--

CREATE TABLE `records` (
  `records_id` int(10) UNSIGNED NOT NULL,
  `record_name` char(50) CHARACTER SET utf8 DEFAULT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `volume` decimal(10,2) UNSIGNED NOT NULL DEFAULT 0.00,
  `wallet_id` int(10) UNSIGNED NOT NULL,
  `action_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `records`
--

INSERT INTO `records` (`records_id`, `record_name`, `datetime`, `volume`, `wallet_id`, `action_id`) VALUES
(2, 'first payday', '2020-05-13 19:41:25', 500.00, 15, 1),
(3, 'shop-time', '2020-05-14 14:22:47', 203.00, 15, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `status`
--

CREATE TABLE `status` (
  `status_id` int(10) UNSIGNED NOT NULL,
  `status_name` char(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `status`
--

INSERT INTO `status` (`status_id`, `status_name`) VALUES
(1, 'user');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `user_id` int(10) UNSIGNED NOT NULL,
  `first_name` char(50) NOT NULL,
  `last_name` char(50) NOT NULL,
  `login` char(50) CHARACTER SET utf8 NOT NULL,
  `email` char(100) NOT NULL,
  `password` char(100) NOT NULL,
  `status_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `login`, `email`, `password`, `status_id`) VALUES
(2, 'Артем', 'Шадчнев', 'enderfun', 'ww@ww.ww', 'hello', 1),
(5, 'RAK', 'PAK', 'stormRak', 'storm@rak.pak', '849c829d658baaeff512d766b0db3cce', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `wallet`
--

CREATE TABLE `wallet` (
  `wallet_id` int(10) UNSIGNED NOT NULL,
  `wallet_name` char(31) CHARACTER SET utf8 NOT NULL,
  `wallet_owner_id` int(10) UNSIGNED NOT NULL,
  `wallet_currency_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `wallet`
--

INSERT INTO `wallet` (`wallet_id`, `wallet_name`, `wallet_owner_id`, `wallet_currency_id`) VALUES
(12, 'FFFFF', 2, 1),
(15, 'storm wallet', 5, 2),
(18, 'My family budget', 5, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `wallet_access`
--

CREATE TABLE `wallet_access` (
  `wallet_access_id` int(10) UNSIGNED NOT NULL,
  `wallet_id` int(10) UNSIGNED NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `access_level_id` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `wallet_access`
--

INSERT INTO `wallet_access` (`wallet_access_id`, `wallet_id`, `user_id`, `access_level_id`) VALUES
(7, 12, 2, 1),
(10, 15, 5, 1),
(13, 18, 5, 1),
(20, 15, 2, 1);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `access_lvl`
--
ALTER TABLE `access_lvl`
  ADD PRIMARY KEY (`access_level_id`),
  ADD UNIQUE KEY `access_level_id` (`access_level_id`);

--
-- Индексы таблицы `action`
--
ALTER TABLE `action`
  ADD PRIMARY KEY (`action_id`),
  ADD UNIQUE KEY `action_id` (`action_id`);

--
-- Индексы таблицы `currency`
--
ALTER TABLE `currency`
  ADD PRIMARY KEY (`currency_id`),
  ADD UNIQUE KEY `currency_id` (`currency_id`);

--
-- Индексы таблицы `records`
--
ALTER TABLE `records`
  ADD PRIMARY KEY (`records_id`),
  ADD UNIQUE KEY `records_id` (`records_id`),
  ADD KEY `FK_wallet` (`wallet_id`),
  ADD KEY `FK_action` (`action_id`);

--
-- Индексы таблицы `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`status_id`),
  ADD UNIQUE KEY `status_id` (`status_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `unique` (`email`),
  ADD UNIQUE KEY `unique_login` (`login`),
  ADD KEY `FK` (`status_id`);

--
-- Индексы таблицы `wallet`
--
ALTER TABLE `wallet`
  ADD PRIMARY KEY (`wallet_id`),
  ADD UNIQUE KEY `wallet` (`wallet_id`),
  ADD KEY `FK__users` (`wallet_owner_id`),
  ADD KEY `FK_currency` (`wallet_currency_id`);

--
-- Индексы таблицы `wallet_access`
--
ALTER TABLE `wallet_access`
  ADD PRIMARY KEY (`wallet_access_id`),
  ADD UNIQUE KEY `wallet_access_id` (`wallet_access_id`),
  ADD KEY `FK_wallet_access` (`wallet_id`),
  ADD KEY `FK_user_access` (`user_id`),
  ADD KEY `FK_access_level` (`access_level_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `access_lvl`
--
ALTER TABLE `access_lvl`
  MODIFY `access_level_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `action`
--
ALTER TABLE `action`
  MODIFY `action_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `currency`
--
ALTER TABLE `currency`
  MODIFY `currency_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `records`
--
ALTER TABLE `records`
  MODIFY `records_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `status`
--
ALTER TABLE `status`
  MODIFY `status_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `wallet`
--
ALTER TABLE `wallet`
  MODIFY `wallet_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT для таблицы `wallet_access`
--
ALTER TABLE `wallet_access`
  MODIFY `wallet_access_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `records`
--
ALTER TABLE `records`
  ADD CONSTRAINT `FK_action` FOREIGN KEY (`action_id`) REFERENCES `action` (`action_id`),
  ADD CONSTRAINT `FK_wallet` FOREIGN KEY (`wallet_id`) REFERENCES `wallet` (`wallet_id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `FK` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`);

--
-- Ограничения внешнего ключа таблицы `wallet`
--
ALTER TABLE `wallet`
  ADD CONSTRAINT `FK__users` FOREIGN KEY (`wallet_owner_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_currency` FOREIGN KEY (`wallet_currency_id`) REFERENCES `currency` (`currency_id`);

--
-- Ограничения внешнего ключа таблицы `wallet_access`
--
ALTER TABLE `wallet_access`
  ADD CONSTRAINT `FK_access_level` FOREIGN KEY (`access_level_id`) REFERENCES `access_lvl` (`access_level_id`),
  ADD CONSTRAINT `FK_user_access` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_wallet_access` FOREIGN KEY (`wallet_id`) REFERENCES `wallet` (`wallet_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
