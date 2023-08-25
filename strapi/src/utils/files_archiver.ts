var JSZip = require("jszip");

export interface DataToArchive {
  data: string;
  file_name: string;
}

export async function createArchiveAndCollectContent(
  data: DataToArchive[]
): Promise<Uint8Array> {
  const zip = new JSZip();

  for (let i = 0; i < data.length; i++) {
    zip.file(data[i].file_name, data[i].data);
  }

  const zipData = await zip.generateAsync({ type: "uint8array" });

  return zipData;
}
