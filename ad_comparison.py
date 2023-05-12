import csv
import os
from util import HeatMapGenerator


class CreateHeatmap:
    def __init__(self, matrixFile):
        self.matrixFile = matrixFile
        self.period = str()
        self.scriptToRun = str()
        self.fileBody = list()
        self.body612_ = list()
        self.body212_ = list()
        self.body26_ = list()
        self.heads2mVersus6m = [
            "Species",
            "2AD-2m_S6",
            "4AD-2m_S2",
            "5AD-2m_S7",
            "8AD-2m_S8",
            "9AD-2m_S9",
            "10AD-2m_S10",
            "2AD-6m_S5",
            "4AD-6m_S7",
            "5AD-6m_S6",
            "8AD-6m_S8",
            "9AD-6m_S9",
            "10AD-6m_S10",
        ]

        self.heads2mVersus12m = [
            "Species",
            "2AD-2m_S6",
            "4AD-2m_S2",
            "5AD-2m_S7",
            "8AD-2m_S8",
            "9AD-2m_S9",
            "10AD-2m_S10",
            "2AD-12m_S7",
            "5AD-12m_S8",
            "6AD-12m_S9",
            "8AD-12m_S10",
            "9AD-12m_S11",
            "10AD-12m_S12",
        ]

        self.heads6MVersus12m = [
            "Species",
            "2AD-6m_S5",
            "4AD-6m_S7",
            "5AD-6m_S6",
            "8AD-6m_S8",
            "9AD-6m_S9",
            "10AD-6m_S10",
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
            for filename in os.listdir("ad_data")
            if filename.endswith(".csv")
            and filename.__contains__("_AD_versus_")
        ]

        for file in filePool:
            splits = file.split("_")
            self.period = splits[0].split('m')[0] + splits[3].split('m')[0]

            # 612 --> 6 months versus 12 months
            # 212 --> 2 months versus 12 months
            # 26 --> 2 months versus 6 months

            with open(f"ad_data/{file}", "r") as csvfile:
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
            tempFile = f"ad_TEMP/Test-{self.period}-Months_TEMPFILE.csv"

            with open(tempFile, "w", newline="") as csvfile:
                fieldnames = ["", "log2FC", "lfcSE", "Pvalues", "FDR"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)

            org = [x[""] for x in rows]

            with open(tempFile) as tempo:
                temp_contents = tempo.readlines()[1:]
            #
            significant_species = [
                f"s__{x.split(',')[0].strip()}" for x in temp_contents
            ]

            with open(self.matrixFile) as mp:
                matrix = mp.readlines()[1:]

            for line in matrix:
                speciesFromMatrix = line.split("\t")[0].split(";")[-1]

                for significantSpecies in significant_species:
                    if speciesFromMatrix == significantSpecies:
                        rawRowContent = line.split("\t")
                        if self.period == "612":
                            rowContent = [y.strip() for y in rawRowContent[19:25]] + [x.strip() for x in rawRowContent[31:]]
                            rowContent.insert(0, speciesFromMatrix)
                            # print(rowContent) -----------------------------------------> Done
                            self.body612_.append(rowContent)

                        elif self.period == "212":
                            rowContent = [y.strip() for y in rawRowContent[7:13]] + [x.strip() for x in rawRowContent[31:]]
                            rowContent.insert(0, speciesFromMatrix)
                            # print(rowContent) -------------------------------------------> Donw
                            self.body212_.append(rowContent)
                        #
                        elif self.period == "26":
                            # rowContent = line.split("\t")[25:]
                            rowContent = [y.strip() for y in rawRowContent[7:13]] + [x.strip() for x in rawRowContent[19:25]]
                            rowContent.insert(0, speciesFromMatrix)
                            # print(rowContent) ----------------------------------> Done
                            self.body26_.append(rowContent)

            if self.period == "612":
                self.scriptToRun = "_612heatmap.R"
                fieldnames = self.heads6MVersus12m
                self.fileBody = self.body612_
            elif self.period == "212":
                self.scriptToRun = "_212heatmap.R"
                fieldnames = self.heads2mVersus12m
                self.fileBody = self.body212_
            #
            elif self.period == "26":
                self.scriptToRun = "_26heatmap.R"
                fieldnames = self.heads2mVersus6m
                self.fileBody = self.body26_

            finalOutputFile = f"AD_{self.period[1]}_Versus_AD_{self.period[1:]}_significant_species.csv"
            #
            with open(finalOutputFile, "w", newline="") as outfile:
                csvwriter = csv.writer(outfile, delimiter="\t")
                csvwriter.writerow(fieldnames)
                csvwriter.writerows(self.fileBody)

            # # Generate Heatmap
            command = [
                "Rscript",
                self.scriptToRun,
                finalOutputFile,
                f"AD {self.period[0]} months Versus AD {self.period[1:]} months",
                f"AD{self.period[0]}_months_Versus_{self.period[1:]}_months_Heatmap.pdf",
            ]
            #
            heatmap = HeatMapGenerator(command)

            heatmap.generateHeatmap()


if __name__ == "__main__":
    # pass
    x = CreateHeatmap("data/metaphlan_matrix.csv")
    x.start()
    # In it's present implementation, this should work fine.
