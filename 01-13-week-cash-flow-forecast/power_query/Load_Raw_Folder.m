let
    SourceFolder = "C:\\path\\to\\01-13-week-cash-flow-forecast\\data\\raw",
    Files = Folder.Files(SourceFolder),
    CsvFiles = Table.SelectRows(Files, each [Extension] = ".csv"),
    AddTables = Table.AddColumn(CsvFiles, "Data", each Csv.Document([Content], [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv])),
    PromoteHeaders = Table.TransformColumns(AddTables, {"Data", each Table.PromoteHeaders(_, [PromoteAllScalars=true])}),
    SelectColumns = Table.SelectColumns(PromoteHeaders, {"Name", "Data"}),
    RenameColumns = Table.RenameColumns(SelectColumns, {{"Name", "SourceFile"}})
in
    RenameColumns
