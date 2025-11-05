INSERT INTO public.products (db_id, name, deskripsi, type, code, isactive, uripath, method, created_at, updated_at) 
values ('40e6215d-b5c6-4896-987c-f30f3678f608','Balance-Inquiry', 'API Balance Inquiry', 'sandbox', '001', True, '/api/v1.0/balance-inquiry', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3678f609', 'Account-Inquiry','API Account Inquiry', 'sandbox', '002', True, '/api/v1.0/account-inquiry', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3678f60a','IntraBank-Transfer','API IntraBank Transfer', 'sandbox', '003', True, '/api/v1.0/transfer-intrabank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3678f60b', 'InterBank-Transfer','API InterBank Transfer', 'sandbox', '004', True, '/api/v1.0/transfer-interbank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3678f60c', 'Status-Transfer','API Status Transfer', 'sandbox', '005', True, '/api/v1.0/transfer/status', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3678f60d', 'Transaction-History-List','API Transaction History List', 'sandbox', '006', True, '/api/v1.0/transaction-history-list', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3678f60e', 'Transaction-History-Details','API Transaction History Details', 'sandbox', '007', True, '/api/v1.0/transaction-history-detail', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3679f608', 'Balance-Inquiry', 'API Balance Inquiry', 'production', '101', True, '/api/v1.0/balance-inquiry',  'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3679f609', 'Account-Inquiry','API Account Inquiry', 'production', '102', True, '/api/v1.0/account-inquiry',  'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3679f60a', 'IntraBank-Transfer','API IntraBank Transfer', 'production', '103', True, '/api/v1.0/transfer-intrabank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3679f60b', 'InterBank-Transfer','API InterBank Transfer', 'production', '104', True, '/api/v1.0/transfer-interbank', 'POST', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3679f60c', 'Status-Transfer','API Status Transfer', 'production', '105', True, '/api/v1.0/transfer/status', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3679f60d', 'Transaction-History-List','API Transaction History List', 'production', '106', True, '/api/v1.0/transaction-history-list',  'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('40e6215d-b5c6-4896-987c-f30f3679f60e', 'Transaction-History-Details','API Transaction History Details', 'production', '107', True, '/api/v1.0/transaction-history-detail', 'GET', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

