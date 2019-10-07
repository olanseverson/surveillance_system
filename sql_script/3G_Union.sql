(select
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName,a.RNC,a.WBTS,a.WCEL,a.IPNBId,a.PtxCellMax,a.MBLBStateTransEnabled,"newXXX" AS Remark
from isat_tmp.susy3G_today a 
Join isat_tmp.susy3G_yesterday b 
On a.oss = b.oss and a.rnc = b.rnc and a.wbts = b.wbts and a.WCEL = b.WCEL
WHERE (a.NAME  LIKE '%XXX%' ) AND (b.NAME NOT LIKE '%XXX%') 
group by a.oss, a.rnc, b.rnc, a.wbts, b.wbts, a.WCEL, b.WCEL
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName,a.RNC,a.WBTS,a.WCEL,a.IPNBId,a.PtxCellMax,a.MBLBStateTransEnabled,"newXYX" AS Remark
from isat_tmp.susy3G_today a 
Join isat_tmp.susy3G_yesterday b 
On a.oss = b.oss and a.rnc = b.rnc and a.wbts = b.wbts and a.WCEL = b.WCEL
WHERE (a.NAME  LIKE '%XYX%' ) AND (b.NAME NOT LIKE '%XYX%') 
group by a.oss, a.rnc, b.rnc, a.wbts, b.wbts, a.WCEL, b.WCEL
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName,a.RNC,a.WBTS,a.WCEL,a.IPNBId,a.PtxCellMax,a.MBLBStateTransEnabled,"removalXXX" AS Remark
from isat_tmp.susy3G_today a 
Join isat_tmp.susy3G_yesterday b 
On a.oss = b.oss and a.rnc = b.rnc and a.wbts = b.wbts and a.WCEL = b.WCEL
WHERE (b.NAME LIKE '%XXX%') AND (a.NAME NOT LIKE '%XYX%' ) AND (a.NAME NOT LIKE '%XXX%') 
group by a.oss, a.rnc, b.rnc, a.wbts, b.wbts, a.WCEL, b.WCEL
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName,a.RNC,a.WBTS,a.WCEL,a.IPNBId,a.PtxCellMax,a.MBLBStateTransEnabled,"removalXXX" AS Remark
from isat_tmp.susy3G_today a 
Join isat_tmp.susy3G_yesterday b 
On a.oss = b.oss and a.rnc = b.rnc and a.wbts = b.wbts and a.WCEL = b.WCEL
WHERE (b.NAME LIKE '%XYX%') AND (a.NAME NOT LIKE '%XYX%' ) AND (a.NAME NOT LIKE '%XXX%') 
group by a.oss, a.rnc, b.rnc, a.wbts, b.wbts, a.WCEL, b.WCEL
)