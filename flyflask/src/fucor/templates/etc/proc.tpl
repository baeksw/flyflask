CREATE OR REPLACE PROCEDURE KTR_DEV."SP_GEN_NUMBER_FA" (
		 iSYST_LNCD		IN VARCHAR2		/* 시스템언어코드*/
		,iUPDT_USID		IN VARCHAR2		/* 수정작업자*/
		,iSTDS_DATE		IN VARCHAR2		/* 기준일자*/
		,iACGN_TYCD		IN VARCHAR2		/* 회계채번유형코드*/
		,iACGN_STXT		IN VARCHAR2		/* 회계채번보조문자열*/
        ,oACGN_NUMB    OUT VARCHAR2		/* 회계채번번호*/
   	)
    /******************************************************************************
		 NAME:       SP_GEN_NUMBER_FA
		 PURPOSE:    번호생성
		 REVISIONS:
		 Ver        Date        Author           Description
		 ---------  ----------  ---------------  ------------------------------------
		 1.0        2016-07-20             1. Created this package.
	 ******************************************************************************/
	IS

		LV_SQRN			NUMBER(6);	/* 일련번호*/
		LV_ACGN_STXT	TA_NUMBXM.ACGN_STXT%TYPE; /* 회계채번보조문자열*/

	BEGIN

		LV_ACGN_STXT 	:= iACGN_STXT; /* 회계채번보조문자열*/

		/* 전표번호채번*/
		IF iACGN_TYCD = 'SLIP_NUMB' THEN

			LV_ACGN_STXT	:= 'GL';

			SELECT	TO_NUMBER(NVL(MAX(SUBSTR(SM.ACGN_NUMB,-6)),'0')) + 1
			INTO	LV_SQRN
			FROM	TA_NUMBXM SM
			WHERE	1 = 1
			AND		SM.STDS_DATE = iSTDS_DATE /* 전표일자 = 기준일자  */
			AND		SM.ACGN_STXT = LV_ACGN_STXT /* GL = 회계채번보조문자열*/
			AND		SM.ACGN_TYCD = iACGN_TYCD /* 회계채번유형코드*/
			;

			/* 번호생성*/
			oACGN_NUMB := LV_ACGN_STXT || iSTDS_DATE || LPAD(LV_SQRN,6,'0');

		/* 결의번호채번*/
		ELSIF iACGN_TYCD = 'RSLR_NUMB' THEN

			LV_ACGN_STXT	:= 'TG';

			SELECT	TO_NUMBER(NVL(MAX(SUBSTR(SM.ACGN_NUMB,-6)),'0')) + 1
			INTO	LV_SQRN
			FROM	TA_NUMBXM SM
			WHERE	1 = 1
			AND		SM.STDS_DATE = iSTDS_DATE /* 결의일자 = 기준일자  */
			AND		SM.ACGN_STXT = LV_ACGN_STXT /* GL = 회계채번보조문자열*/
			AND		SM.ACGN_TYCD = iACGN_TYCD /* 회계채번유형코드*/
			;

			/* 번호생성*/
			oACGN_NUMB := LV_ACGN_STXT || iSTDS_DATE || LPAD(LV_SQRN,6,'0');

		END IF;

        /* 회계공용번호채번 */
        UPDATE  TA_NUMBXM SET
                 ACGN_NUMB   = oACGN_NUMB    /* 회계채번번호 */
                ,UPDT_USID   = iUPDT_USID    /* 수정작업자 */
                ,UPDT_DATE   = SYSDATE       /* 수정일시 */
        WHERE   1 = 1
        AND     STDS_DATE    = iSTDS_DATE    /* 기준일 */
        AND     ACGN_TYCD    = iACGN_TYCD    /* 회계채번유형코드[ACGN_TYCD] */
        AND     ACGN_STXT    = LV_ACGN_STXT  /* 회계채번보조문자열 */
		;

		IF SQL%ROWCOUNT = 0 THEN
			/* 회계공용번호채번 */
			INSERT INTO TA_NUMBXM (
				 STDS_DATE          /* 기준일 */
				,ACGN_TYCD          /* 회계채번유형코드[ACGN_TYCD] */
				,ACGN_STXT          /* 회계채번보조문자열 */
				,ACGN_NUMB          /* 회계채번번호 */
				,INST_USID          /* 입력작업자 */
				,INST_DATE          /* 입력일시 */
				,UPDT_USID          /* 수정작업자 */
				,UPDT_DATE          /* 수정일시 */
				)
			VALUES
				(
				 iSTDS_DATE       /* 기준일 */
				,iACGN_TYCD       /* 회계채번유형코드[ACGN_TYCD] */
				,LV_ACGN_STXT     /* 회계채번보조문자열 */
				,oACGN_NUMB       /* 회계채번번호 */
				,iUPDT_USID       /* 입력작업자 */
				,SYSDATE            /* 입력일시 */
				,iUPDT_USID       /* 수정작업자 */
				,SYSDATE            /* 수정일시 */
				);
		END IF;

	END;
/
