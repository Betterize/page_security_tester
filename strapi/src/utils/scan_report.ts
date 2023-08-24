import fs from "fs";
import handlebars from "handlebars";

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
  is_public: boolean;
  website: string;
  email: string;
  createdAt: string;
  updatedAt: string;
  error_msg: null | object;
  status: string;
  tests_results: ScanTestResult[];
}

export enum ReportPart {
  Main = "main",
  Nmap = "nmap",
  NmapHostname = "nmap/hostname",
  NmapPort = "nmap/port",
  Wapiti = "wapiti",
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

function buildWapiti(data: Object) {
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

function findTestResults(data: ScanReport, test: string) {
  return data.tests_results.find((element) => element.tool == test);
}

// ----------------------------------------------------------

export async function buildReport(data: ScanReport) {
  try {
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

    const t = report_templates["main"](template_base);
    console.log(t);
  } catch (e) {
    console.log(e);
  }
}
