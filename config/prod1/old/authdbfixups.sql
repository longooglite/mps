UPDATE application SET url = 'https://${site}.mntnpass.com/appt' WHERE code = 'APPT';
UPDATE application SET url = 'https://${site}.mntnpass.com/imm' WHERE code = 'IMM';
UPDATE application SET url = 'https://${site}.mntnpass.com/cv' WHERE code = 'CV';
UPDATE application SET url = 'https://${site}.mntnpass.com/admin' WHERE code = 'MPSADMIN';
DELETE FROM site_preference WHERE site_code <> '' AND site_code <> 'cmich';
DELETE FROM site_application WHERE site_id <> (SELECT id FROM site WHERE code = 'cmich');
UPDATE mpsuser SET password = 'a727e263c03ad62401fa91ee4aee363a10211113d07160a5f0ae5f03312aa240' WHERE site_id=2 and username NOT IN ('mpsadmin','Test-one45','mpldap');
