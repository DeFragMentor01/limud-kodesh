﻿CREATE TABLE [dbo].[Taamim_Ref]
(
	[TaamID] INT NOT NULL PRIMARY KEY, 
    [Taam] NVARCHAR(50) NOT NULL, 
    [TaamName] NVARCHAR(50) NOT NULL, 
    [Comments] NVARCHAR(MAX) NULL
)

GO
EXEC sp_addextendedproperty @name = N'MS_Description',
    @value = N'הניקוד עצמו בUTF-8',
    @level0type = N'SCHEMA',
    @level0name = N'dbo',
    @level1type = N'TABLE',
    @level1name = N'Taamim_Ref',
    @level2type = N'COLUMN',
    @level2name = N'Taam'
GO
EXEC sp_addextendedproperty @name = N'MS_Description',
    @value = N'מזהה קוד פנימי עבור הטעם',
    @level0type = N'SCHEMA',
    @level0name = N'dbo',
    @level1type = N'TABLE',
    @level1name = N'Taamim_Ref',
    @level2type = N'COLUMN',
    @level2name = N'TaamID'
GO
EXEC sp_addextendedproperty @name = N'MS_Description',
    @value = N'שם הטעם כגון זקף קטון וכדומה',
    @level0type = N'SCHEMA',
    @level0name = N'dbo',
    @level1type = N'TABLE',
    @level1name = N'Taamim_Ref',
    @level2type = N'COLUMN',
    @level2name = N'TaamName'