import fs from "fs";
import handlebars from "handlebars";
import {
  DataToArchive,
  createArchiveAndCollectContent,
} from "./files_archiver";

interface ScanTestResult {
  id: number;
  tool: string;
  scan_time: string;
  command: string;
  result: [Object];
  status: string;
}

export interface ScanReport {
  id: number;
  accepted_regulations: boolean;
  website: string;
  email: string;
  createdAt: string;
  updatedAt: string;
  error_msg: null | object;
  status: string;
  tests_results: ScanTestResult[];
  createdBy: Object;
  updatedBy: Object;
}

export enum ReportPart {
  Main = "main",
  Nmap = "nmap",
  NmapHostname = "nmap/hostname",
  NmapPort = "nmap/port",
  Wapiti = "wapiti",
  WapitiInfos = "wapiti/infos",
  WapitiSection = "wapiti/section",
}

// ----------------------------------------------------------

function load_templates() {
  const enum_values = Object.values(ReportPart) as string[];
  let result = {};

  for (let key of enum_values) {
    let data = fs.readFileSync(
      `./src/utils/scan_report_templates/${key}.html`,
      "utf-8"
    );

    result[key] = handlebars.compile(data);
  }

  return result;
}

var report_templates = load_templates();

// ----------------------------------------------------------

function buildNmap(data: Object) {
  const hosts = data["result"]["host_names"].map(
    (host) =>
      new handlebars.SafeString(
        report_templates[ReportPart.NmapHostname]({ host: host })
      )
  );

  const ports = data["result"]["ports"].map((port) => {
    for (const key in port["service"]) {
      if (port["service"][key] === null) {
        port["service"][key] = "No info";
      }
    }

    return new handlebars.SafeString(
      report_templates[ReportPart.NmapPort]({ port: port })
    );
  });

  return new handlebars.SafeString(
    report_templates[ReportPart.Nmap]({ hosts: hosts, ports: ports })
  );
}

// ----------------------------------------------------------
function getSections(sections: Object) {
  const result = Object.keys(sections)
    .filter((key) => key != "infos")
    .map((section_name) => {
      const data = Object.keys(sections[section_name]).map((category) => {
        var res = [];

        const raw_blocks = sections[section_name][category];

        if (raw_blocks.length > 0) {
          for (const index in raw_blocks) {
            const fields = Object.keys(raw_blocks[index])
              .filter((element) => element != "http_request")
              .map((element) => {
                return {
                  name: element,
                  data: raw_blocks[index][element]
                    ? raw_blocks[index][element]
                    : "No info",
                };
              });
            res.push({
              fields: fields,
              request: raw_blocks[index].http_request,
            });
          }
        }

        return { key: category, blocks: res };
      });

      return new handlebars.SafeString(
        report_templates[ReportPart.WapitiSection]({
          name: section_name,
          data: data,
        })
      );
    });

  return result;
}

function getWapitiInfos(infos: Object) {
  const excludedKeys = ["auth", "detailed_report"];

  const result = Object.keys(infos)
    .filter((key) => !excludedKeys.includes(key))
    .map((key) => {
      const modifiedKey = key === "crawled_pages_nbr" ? "crawled_pages" : key;
      return {
        name: modifiedKey,
        value: infos[key],
      };
    });

  return result;
}

function buildWapiti(data: Object) {
  const infos = new handlebars.SafeString(
    report_templates[ReportPart.WapitiInfos]({
      infos: getWapitiInfos(data["result"]["infos"]),
    })
  );

  return new handlebars.SafeString(
    report_templates[ReportPart.Wapiti]({
      infos: infos,
      sections: getSections(data["result"]),
    })
  );
}

// ----------------------------------------------------------

function findTestResults(data: ScanReport, test: string) {
  return data.tests_results.find((element) => element.tool == test);
}

// ----------------------------------------------------------

function buildReport(data: ScanReport) {
  var template_base = {
    email: data.email,
    website: data.website,
  };

  const nmap_data = findTestResults(data, "nmap");

  if (nmap_data != undefined && nmap_data.status == "finished") {
    const nmap_template = buildNmap(nmap_data);

    template_base["nmap"] = nmap_template;
  }

  const wapiti_data = findTestResults(data, "wapiti");

  if (wapiti_data != undefined && wapiti_data.status == "finished") {
    const wapiti_template = buildWapiti(wapiti_data);

    template_base["wapiti"] = wapiti_template;
  }

  return report_templates["main"](template_base);
}

// ----------------------------------------------------------

export async function getReport(data: ScanReport) {
  const report = buildReport(data);

  const result = await createArchiveAndCollectContent([
    { data: report, file_name: "scan_result.html" },
  ]);
  return result;
}
