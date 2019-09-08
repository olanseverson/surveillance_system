TRUNCATE isat_tmp.susy2G_yesterday;
REplace into isat_tmp.susy2G_yesterday
select a.oss,a.xdate,c.SITE_ID,a.name,a.BSC,a.BCF,a.BTS,b.TRX,a.frequencyBandInUse
from isat_cm.bts a 
Join isat_cm.trx b 
On a.oss = b.oss and  a.xdate = b.xdate and a.bsc = b.bsc and a.bcf = b.bcf and a.bts = b.bts 
Join isat_adm.t_list_2g_profile c 
on a.bsc = c.bscid and a.bcf = c.bcfid and a.bts = c.btsid
where a.xdate = '2019-08-28' 
group by a.oss,a.xdate, a.BSC,a.BCF,a.BTS,b.TRX
;