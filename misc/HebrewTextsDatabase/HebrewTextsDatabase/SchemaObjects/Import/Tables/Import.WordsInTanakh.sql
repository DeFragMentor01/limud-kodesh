﻿CREATE TABLE [Import].[WordsInTanakh] (
    [ID]             INT            NOT NULL,
    [Word]           NVARCHAR (50)  NOT NULL,
    [WordWithNiqqud] NVARCHAR (MAX) NOT NULL,
    [VerseID]        INT            NOT NULL,
    [SequenceNumber] INT            NULL,
    CONSTRAINT [PK_WordsInTanakh] PRIMARY KEY CLUSTERED ([ID] ASC)
);


GO
CREATE NONCLUSTERED INDEX [idx_WordsInTanakh_Word]
    ON [Import].[WordsInTanakh]([Word] ASC);


GO
CREATE NONCLUSTERED INDEX [OldID]
    ON [Import].[WordsInTanakh]([ID] ASC);

