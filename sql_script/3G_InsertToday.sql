TRUNCATE isat_tmp.susy3G_today;
REPLACE INTO isat_tmp.susy3G_today
select a.oss,a.xdate,c.SITE_ID,a.name,a.RNC,a.WBTS,a.WCEL,b.IPNBId,a.PtxCellMax,a.MBLBStateTransEnabled
from isat_cm.wcel a Join isat_cm.wbts b 
On a.oss = b.oss and  a.xdate = b.xdate and a.rnc = b.rnc and a.wbts = b.wbts 
Join isat_adm.t_list_3g_profile c on a.rnc = c.rnc_id and a.wbts = c.wbts_id and a.WCEL = c.CELL_ID
where a.xdate = '2019-08-29'
group by  a.oss,a.xdate, a.RNC,a.WBTS,a.WCEL
;