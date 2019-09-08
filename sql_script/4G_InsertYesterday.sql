TRUNCATE isat_tmp.susy4G_yesterday;
Replace into isat_tmp.susy4G_yesterday
select a.oss,a.xdate,c.SITE_ID,a.name, a.cellname, a.MRBTS,a.lnbts,a.LNCEL,b.earfcnDL,b.dlchbw, a.pMax 
from isat_cm.lncel a 
Join isat_cm.LNcel_fdd b 
On a.oss = b.oss and  a.xdate = b.xdate and a.LNBTS = b.lnbts and a.MRBTS = b.mrbts and a.LNCEL = b.lncel
Join isat_adm.t_list_4g_profile c on a.mrbts = c.MRBTS_ID and a.lncel = c.LNCEL_ID
where a.xdate = '2019-08-28'
group by a.oss,a.xdate, a.MRBTS,a.lnbts,a.LNCEL
;
