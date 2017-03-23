CREATE OR REPLACE FUNCTION KTR_DEV."SF_GET_COMMHEADNAME" (
    iCOMM_CODE   IN VI_COMMCODE.COMM_CODE%TYPE
)

RETURN VARCHAR2 IS
RET_NAME  VI_COMMCODE.COMM_CDNM%TYPE;

/******************************************************************************
   NAME      :  SF_GET_COMMHEADNAME
   PURPOSE :  공통 HEAD CODE의 명칭 반환

   REVISIONS:
   Ver            Date            Author                           Description
   ---  --------------   ---------------  ------------------------------------
   1.0      2016-08-26            김석두              1. Created this function.

   NOTES:
   * 코드가 없다면 입력된 코드를 그대로 보여준다.
******************************************************************************/
BEGIN

   RET_NAME := RET_NAME;

   BEGIN

      SELECT COMM_CDNM
        INTO RET_NAME
        FROM TM_CODEXH
       WHERE COMM_CODE = iCOMM_CODE;

   EXCEPTION

      WHEN NO_DATA_FOUND THEN
           RET_NAME :=  RET_NAME;
      WHEN OTHERS THEN
           RET_NAME :=  RET_NAME;

   END;

   RETURN RET_NAME;

END SF_GET_COMMHEADNAME;
/
