DROP TABLE IF EXISTS gv_gs_award_reporting_v1;
CREATE TABLE gv_gs_award_reporting_v1 (
  award_id TEXT,
  program_name TEXT,
  award_status TEXT,
  fiscal_year INTEGER,
  award_date TEXT,
  amount_awarded REAL,
  steward_org_id TEXT
);
INSERT INTO gv_gs_award_reporting_v1 VALUES
('AWD-100','Program A','active',2023,'2023-01-15',100000,'ORG-1'),
('AWD-101','Program A','active',2023,'2023-02-10',125000,'ORG-1'),
('AWD-102','Program B','active',2023,'2023-03-11',50000,'ORG-1'),
('AWD-103','Program C','closed',2022,'2022-09-01',45000,'ORG-1');

DROP TABLE IF EXISTS gv_gs_amendment_delta_v1;
CREATE TABLE gv_gs_amendment_delta_v1 (
  award_id TEXT,
  amendment_id TEXT,
  amendment_type TEXT,
  delta_amount REAL,
  fiscal_quarter TEXT,
  approval_status TEXT
);
INSERT INTO gv_gs_amendment_delta_v1 VALUES
('AWD-100','AMD-1','budget',5000,'Q2','approved'),
('AWD-101','AMD-2','funding_change',8000,'Q2','approved'),
('AWD-102','AMD-3','scope',1000,'Q1','pending');

DROP TABLE IF EXISTS gv_gs_closeout_compliance_v1;
CREATE TABLE gv_gs_closeout_compliance_v1 (
  award_id TEXT,
  program_name TEXT,
  days_overdue INTEGER,
  blocker_code TEXT,
  blocker_text TEXT,
  closeout_state TEXT
);
INSERT INTO gv_gs_closeout_compliance_v1 VALUES
('AWD-100','Program A',14,'DOC','Missing docs','blocked'),
('AWD-101','Program B',0,'','', 'on_track'),
('AWD-102','Program C',45,'FIN','Awaiting final invoice','blocked');
