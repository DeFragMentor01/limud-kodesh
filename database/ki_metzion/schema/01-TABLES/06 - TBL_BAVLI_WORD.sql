USE KiMeTzion;

SET NOCOUNT ON;

DROP TABLE IF EXISTS TBL_BAVLI_WORD

CREATE TABLE TBL_BAVLI_WORD
(
BAVLI_WORD_ID INT NOT NULL IDENTITY 
,MASSECHET_DAF_ID INT NOT NULL
,PEREK_ID INT NOT NULL
,ROW_ID INT NOT NULL
,W_DELETED bit NOT NULL
,W_ADDED bit NOT NULL
,WORD_POSITION INT NOT NULL
,WORD_TYPE BIT NOT NULL -- 0 mishna or 1 gemara
,WORD NVARCHAR (50) NOT NULL
,CONSTRAINT PK_BAVLI_WORD PRIMARY KEY (BAVLI_WORD_ID)
,CONSTRAINT FK_BAVLI_WORD_MASSECHET_DAF_ID FOREIGN KEY (MASSECHET_DAF_ID) REFERENCES TBL_MASSECHET_DAF (MASSECHET_DAF_ID)
,CONSTRAINT FK_BAVLI_WORD_MASSECHET_PEREK_ID FOREIGN KEY (PEREK_ID) REFERENCES TBL_MASSECHET_PEREK (PEREK_ID)
,INDEX IDX_TBL_BAVLI_WORD_WORD (WORD)
,INDEX IDX_TBL_BAVLI_WORD_ROW_ID (ROW_ID)
,INDEX IDX_TBL_BAVLI_WORD_WORD_ID (WORD_ID)
,INDEX IDX_TBL_BAVLI_WORD_WORD_POSITION (WORD_POSITION)
);
