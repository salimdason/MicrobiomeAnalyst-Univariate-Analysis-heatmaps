import csv
import os
from util import HeatMapGenerator


class CreateHeatmap:
    def __init__(self, matrixFile):
        self.matrixFile = matrixFile
        self.period = str()
        self.scriptToRun = str()
        self.fileBody = list()
        self.bodyTwelveMonths = list()
        self.bodyTwoMonths = list()
        self.bodySixMonths = list()
        self.twoMonthsFields = [
            "Species",
            "2WT-2m_S1",
            "3WT-2m_S1",
            "5WT-2m_S2",
            "8WT-2m_S3",
            "9WT-2m_S4",
            "10WT-2m_S5",
            "2AD-2m_S6",
            "4AD-2m_S2",
            "5AD-2m_S7",
            "8AD-2m_S8",
            "9AD-2m_S9",
            "10AD-2m_S10",
        ]

        self.sixMonthsFields = [
            "Species",
            "2WT-6m_S11",
            "3WT-6m_S1",
            "5WT-6m_S12",
            "8WT-6m_S2",
            "9WT-6m_S3",
            "10WT-6m_S4",
            "2AD-6m_S5",
            "4AD-6m_S7",
            "5AD-6m_S6",
            "8AD-6m_S8",
            "9AD-6m_S9",
            "10AD-6m_S10",
        ]

        self.twelveMonthsFields = [
            "Species",
            "2WT-12m_S1",
            "5WT-12m_S2",
            "6WT-12m_S4",
            "8WT-12m_S3",
            "9WT-12m_S5",
            "10WT-12m_S6",
            "2AD-12m_S7",
            "5AD-12m_S8",
            "6AD-12m_S9",
            "8AD-12m_S10",
            "9AD-12m_S11",
            "10AD-12m_S12",
        ]

    def start(self):
        rowContent = list()

        filePool = [
            filename
            for filename in os.listdir("data")
            if filename.endswith(".csv")
            and filename.__contains__("WT_versus_AD_Species")
        ]

        for file in filePool:
            self.period = file.split("_")[0].split("m")[0]

            with open(f"data/{file}", "r") as csvfile:
                reader = csv.DictReader(csvfile)

                rows = []
                for row in reader:
                    # Convert scientific notation to decimal
                    try:
                        row["Pvalues"] = "{:.40f}".format(float(row["Pvalues"]))
                        row["FDR"] = "{:.40f}".format(float(row["FDR"]))

                        # Conditional Check
                        if (
                            abs(int(float(row["log2FC"]))) > 1
                            and float(row["FDR"]) < 0.05
                        ):
                            rows.append(row)

                    except ValueError:
                        continue

            # Write the updated csv file
            tempFile = f"TEMP/Test-{self.period}-Months_TEMPFILE.csv"

            with open(tempFile, "w", newline="") as csvfile:
                fieldnames = ["", "log2FC", "lfcSE", "Pvalues", "FDR"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)

            org = [x[""] for x in rows]

            with open(tempFile) as tempo:
                temp_contents = tempo.readlines()[1:]

            significant_species = [
                f"s__{x.split(',')[0].strip()}" for x in temp_contents
            ]

            with open(self.matrixFile) as mp:
                matrix = mp.readlines()[1:]

            for line in matrix:
                speciesFromMatrix = line.split("\t")[0].split(";")[-1]

                for significantSpecies in significant_species:
                    if speciesFromMatrix == significantSpecies:
                        if self.period == "2":
                            rowContent = line.split("\t")[1:13]
                            rowContent.insert(0, speciesFromMatrix)
                            self.bodyTwoMonths.append(rowContent)

                        elif self.period == "6":
                            rowContent = line.split("\t")[13:25]
                            rowContent.insert(0, speciesFromMatrix)
                            self.bodySixMonths.append(rowContent)

                        elif self.period == "12":
                            rowContent = line.split("\t")[25:]
                            rowContent.insert(0, speciesFromMatrix)
                            rowContent[-1] = rowContent[-1].strip()
                            self.bodyTwelveMonths.append(rowContent)

            if self.period == "2":
                self.scriptToRun = "two_months_heatmap.R"
                fieldnames = self.twoMonthsFields
                self.fileBody = self.bodyTwoMonths
            elif self.period == "6":
                self.scriptToRun = "six_months_heatmap.R"
                fieldnames = self.sixMonthsFields
                self.fileBody = self.bodySixMonths

            elif self.period == "12":
                self.scriptToRun = "twelve_months_heatmap.R"
                fieldnames = self.twelveMonthsFields
                self.fileBody = self.bodyTwelveMonths

            finalOutputFile = f"{self.period}-Months-significant-species.csv"

            with open(finalOutputFile, "w", newline="") as outfile:
                csvwriter = csv.writer(outfile, delimiter="\t")
                csvwriter.writerow(fieldnames)
                csvwriter.writerows(self.fileBody)

            # Generate Heatmap
            command = [
                "Rscript",
                self.scriptToRun,
                finalOutputFile,
                f"Wild Type versus AD {self.period} months",
                f"{self.period}_month_Heatmap.pdf",
            ]

            heatmap = HeatMapGenerator(command)

            heatmap.generateHeatmap()


if __name__ == "__main__":
    # pass
    x = CreateHeatmap("data/metaphlan_matrix.csv")
    x.start()
