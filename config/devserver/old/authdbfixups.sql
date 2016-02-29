UPDATE application SET url = 'https://${site}.mntnpass.com:447/appt' WHERE code = 'APPT';
UPDATE application SET url = 'https://${site}.mntnpass.com:447/imm' WHERE code = 'IMM';
UPDATE application SET url = 'https://${site}.mntnpass.com:447/cv' WHERE code = 'CV';
UPDATE application SET url = 'https://${site}.mntnpass.com:447/admin' WHERE code = 'MPSADMIN';
UPDATE site_preference SET value = '1800000' WHERE site_code = 'dev' AND code = 'sessionidletimeoutmilliseconds';
UPDATE site_preference SET value = 'ldap://localhost:389/' WHERE site_code = 'dev' AND code = 'ldapurl';
UPDATE site_preference SET value = 'yes' WHERE code = 'authpassreqd';
