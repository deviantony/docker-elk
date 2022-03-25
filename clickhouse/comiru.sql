CREATE DATABASE IF NOT EXISTS `comiru`;
USE `comiru`;

CREATE TABLE IF NOT EXISTS comiru.router_log
(
    `request_id` String,
    `code`       String,
    `desc`       String,
    `path`       String,
    `method`     String,
    `ip`         String,
    `project`    String,
    `status`     Int32,
    `bytes`      Int32,
    `service`    Int32,
    `fwd`        String,
    `host`       String,
    `route`      String,
    `timestamp`  DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;

-- ALTER TABLE `comiru`.`router_log`
--     ADD COLUMN `route_name` String AFTER `host`;
-- ALTER TABLE `comiru`.`router_log`
--     RENAME COLUMN IF EXISTS `route_name` TO `route`;
-- ALTER TABLE `comiru`.`router_log`
--     ADD COLUMN `route` String AFTER `host`;

CREATE TABLE IF NOT EXISTS comiru.operation_log
(
    `user_id`    Int32,
    `user_type`  String,
    `path`       String,
    `route`      String,
    `user_agent` String,
    `request_id` String,
    `session_id` String,
    `ip`         String,
    `input`      String,
    `timestamp`  DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;

-- ALTER TABLE comiru.operation_log
--     ADD COLUMN `session_id` String AFTER `request_id`;

CREATE TABLE IF NOT EXISTS comiru.basic_log
(
    `request_id`          String,
    `status`              Int32,
    `service`             Int32,
    `user_type`           String,
    `user_id`             Int32,
    `path`                String,
    `route`               String,
    `input`               String,
    `host`                String,
    `method`              String,
    `ip`                  String,
    `fwd`                 String,
    `project`             String,
    `bytes`               Int32,
    `user_agent`          String,
    `code`                String,
    `desc`                String,
    `access_timestamp`    DateTime,
    `operation_timestamp` DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS comiru.line_log_v2
(
    `open_id`   String,
    `event`     String,
    `err`       Nullable(String),
    `code`      Nullable(Int32),
    `result`    Nullable(String),
    `data`      String,
    `timestamp` DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS comiru.push_log_v2
(
    `provider`   String,
    `message_id` String,
    `user_type`  String,
    `user_id`    Int32,
    `subject`    String,
    `status`     String,
    `timestamp`  DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS comiru.push_log_v3
(
    `channel`              String,
    `status`               String,
    `id`                   String,
    `msg`                  String,
    `subject`              String,
    `app_type`             String,
    `user_id`              Int32,
    `user_type`            String,
    `user_school_slug`     String,
    `notification_content` String,
    `http_status_code`     Int32,
    `request_id`           String,
    `job_id`               String,
    `timestamp`            DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS comiru.email_log_v2
(
    `provider`   String,
    `message_id` String,
    `subject`    String,
    `to`         String,
    `status`     String,
    `timestamp`  DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS comiru.email_log_v3
(
    `channel`    String,
    `status`     String,
    `id`         Array(String),
    `msg`        String,
    `subject`    String,
    `from`       String,
    `to`         Array(String),
    `task_id`    String,
    `request_id` String,
    `timestamp`  DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;

CREATE TABLE IF NOT EXISTS comiru.worker_log
(
    `name`       String,
    `status`     String,
    `queue`      String,
    `cost`       Float32,
    `retry`      String,
    `msg`        String,
    `job_id`     String,
    `request_id` String,
    `timestamp`  DateTime
)
    ENGINE = MergeTree ORDER BY tuple()
        SETTINGS index_granularity = 8192;
