CREATE TABLE  public.users (
    db_id uuid DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100),
    username VARCHAR(50),
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(50),
    phone VARCHAR(30),
    company VARCHAR(30),
    address VARCHAR(200),
    isactive Boolean,
    avatar VARCHAR(200),
    rolecode = VARCHAR(5),
    max_rate = VARCHAR(10)
    created_at TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (db_id)
)

CREATE TABLE public.apps (
    db_id uuid,
    user_id VARCHAR(100),
    name VARCHAR(100),
    consumer_key VARCHAR(100),
    consumer_secret VARCHAR(200),
    type VARCHAR(15),
    src_accounts VARCHAR(100)[],
    max_rate VARCHAR(10),
    products VARCHAR(100)[],
    expired_at DATE,
    isactive Boolean,
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (db_id)
)

CREATE TABLE public.basecrypto (
    db_id uuid DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100),
    public_key VARCHAR(5000)
    private_key VARCHAR(5000)
    expired_at DATETIME
    isactive Boolean,
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (db_id)

CREATE TABLE public.products (
    db_id uuid DEFAULT uuid_generate_v4(),
    name VARCHAR(100),
    deskripsi VARCHAR(500),
    type VARCHAR(15),
    code VARCHAR(4),
    uripath VARCHAR(100),
    method VARCHAR(10),
    isactive Boolean,
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (db_id)
)

CREATE TABLE public.production_request (
    db_id uuid DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100),
    requested_by VARCHAR(50),
    request_type VARCHAR(50),
    status VARCHAR(50),
    template_file VARCHAR(500),
    final_file VARCHAR(500),
    approved_at DATETIME,
    approved_by VARCHAR(100),
    isactive Boolean,
    created_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (db_id)
)

CREATE TABLE public.app_history (
    db_id uuid DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100),
    content VARCHAR(50),
    content_type VARCHAR(50),
    description VARCHAR(50),
    status VARCHAR(50),
    approved_by VARCHAR(100),
    approved_at DATETIME,
    isactive Boolean,
    created_at TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (db_id)
)


INSERT INTO public.products (db_id, name, deskripsi, type, code, isactive, uripath, method, created_at, updated_at, version) 
values ('40e6215d-b5c6-4896-987c-f30f3678f608','V1.0-Balance-Inquiry', 'API V1.0 Balance Inquiry', 'sandbox', '001', True, '/api/v1.0/balance-inquiry', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3678f607', 'V1.0-Account-Inquiry-External','API V1.0 Account Inquiry External', 'sandbox', '008', True, '/api/v1.0/account-inquiry-external', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3678f609', 'V1.0-Account-Inquiry-Internal','API V1.0 Account Inquiry Internal', 'sandbox', '002', True, '/api/v1.0/account-inquiry-internal', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3678f60a','V1.0-IntraBank-Transfer','API V1.0 IntraBank Transfer', 'sandbox', '003', True, '/api/v1.0/transfer-intrabank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3678f60b', 'V1.0-InterBank-Transfer','API V1.0 InterBank Transfer', 'sandbox', '004', True, '/api/v1.0/transfer-interbank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3678f60c', 'V1.0-Status-Transfer','API V1.0 Status Transfer', 'sandbox', '005', True, '/api/v1.0/transfer/status', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3678f60d', 'V1.0-Transaction-History-List','API V1.0 Transaction History List', 'sandbox', '006', True, '/api/v1.0/transaction-history-list', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3678f60e', 'V1.0-Transaction-History-Details','API V1.0 Transaction History Details', 'sandbox', '007', True, '/api/v1.0/transaction-history-detail', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3679f608', 'V1.0-Balance-Inquiry', 'API V1.0 Balance Inquiry', 'production', '101', True, '/api/v1.0/balance-inquiry',  'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3679f607', 'V1.0-Account-Inquiry-External','API V1.0 Account Inquiry External', 'production', '108', True, '/api/v1.0/account-inquiry-external', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3679f609', 'V1.0-Account-Inquiry-Internal','API V1.0 Account Inquiry Internal', 'production', '102', True, '/api/v1.0/account-inquiry-internal',  'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3679f60a', 'V1.0-IntraBank-Transfer','API V1.0 IntraBank Transfer', 'production', '103', True, '/api/v1.0/transfer-intrabank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3679f60b', 'V1.0-InterBank-Transfer','API V1.0 InterBank Transfer', 'production', '104', True, '/api/v1.0/transfer-interbank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3679f60c', 'V1.0-Status-Transfer','API V1.0 Status Transfer', 'production', '105', True, '/api/v1.0/transfer/status', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3679f60d', 'V1.0-Transaction-History-List','API V1.0 Transaction History List', 'production', '106', True, '/api/v1.0/transaction-history-list',  'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f3679f60e', 'V1.0-Transaction-History-Details','API V1.0 Transaction History Details', 'production', '107', True, '/api/v1.0/transaction-history-detail', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'1.0'),
('40e6215d-b5c6-4896-987c-f30f367af608', 'V2.0-Balance-Inquiry', 'API V2.0 Balance Inquiry', 'sandbox', '201', True, '/api/v2.0/balance-inquiry', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367af607', 'V2.0-Account-Inquiry-External','API V2.0 Account Inquiry External', 'sandbox', '208', True, '/api/v2.0/account-inquiry-external', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367af609', 'V2.0-Account-Inquiry-Internal','API V2.0 Account Inquiry Internal', 'sandbox', '202', True, '/api/v2.0/account-inquiry-internal', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367af60a','V2.0-IntraBank-Transfer','API V2.0 IntraBank Transfer', 'sandbox', '203', True, '/api/v2.0/transfer-intrabank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367af60b', 'V2.0-InterBank-Transfer','API V2.0 InterBank Transfer', 'sandbox', '204', True, '/api/v2.0/transfer-interbank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367af60c', 'V2.0-Status-Transfer','API V2.0 Status Transfer', 'sandbox', '205', True, '/api/v2.0/transfer/status', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367af60d', 'V2.0-Transaction-History-List','API V2.0 Transaction History List', 'sandbox', '206', True, '/api/v2.0/transaction-history-list', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367af60e', 'V2.0-Transaction-History-Details','API V2.0 Transaction History Details', 'sandbox', '207', True, '/api/v2.0/transaction-history-detail', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367bf608', 'V2.0-Balance-Inquiry', 'API V2.0 Balance Inquiry', 'production', '301', True, '/api/v2.0/balance-inquiry',  'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367bf607', 'V2.0-Account-Inquiry-External','API V2.0 Account Inquiry External', 'production', '308', True, '/api/v2.0/account-inquiry-external', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367bf609', 'V2.0-Account-Inquiry-Internal','API V2.0 Account Inquiry Internal', 'production', '302', True, '/api/v2.0/account-inquiry-internal',  'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367bf60a', 'V2.0-IntraBank-Transfer','API V2.0 IntraBank Transfer', 'production', '303', True, '/api/v2.0/transfer-intrabank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367bf60b', 'V2.0-InterBank-Transfer','API V2.0 InterBank Transfer', 'production', '304', True, '/api/v2.0/transfer-interbank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367bf60c', 'V2.0-Status-Transfer','API V2.0 Status Transfer', 'production', '305', True, '/api/v2.0/transfer/status', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367bf60d', 'V2.0-Transaction-History-List','API V2.0 Transaction History List', 'production', '306', True, '/api/v2.0/transaction-history-list',  'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0'),
('40e6215d-b5c6-4896-987c-f30f367bf60e', 'V2.0-Transaction-History-Details','API V2.0 Transaction History Details', 'production', '307', True, '/api/v2.0/transaction-history-detail', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,'2.0');


