﻿CREATE TABLE [dbo].[TBL_TOSSEFOT_WORD] (
    [WORD_ID]            INT           IDENTITY (1, 1) NOT NULL,
    [DIBOUR_HAMATRIL_ID] INT           NOT NULL,
    [WORD]               NVARCHAR (50) NOT NULL,
    CONSTRAINT [PK_TBL_TOSSEFOT_WORD] PRIMARY KEY CLUSTERED ([WORD_ID] ASC),
    CONSTRAINT [FK_TBL_TOSSEFOT_WORD_WORD] FOREIGN KEY ([DIBOUR_HAMATRIL_ID]) REFERENCES [dbo].[TBL_DIBOUR_HAMATRIL] ([DIBOUR_HAMATRIL_ID])
);

