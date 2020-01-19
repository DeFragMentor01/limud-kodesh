USE KiMeTzion;

DROP TABLE IF EXISTS TBL_CONTENT_WORD;

SET NOCOUNT ON; 

CREATE TABLE TBL_CONTENT_WORD
(
CONTENT_WORD_ID INT IDENTITY NOT NULL,
CONTENT_WORD NVARCHAR(100) NOT NULL
CONSTRAINT PK_TBL_CONTENT_WORD_CONTENT_WORD_ID PRIMARY KEY (CONTENT_WORD_ID)
)