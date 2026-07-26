export type Edition = {
  title: string;
  tag: string;
  hue: number;
  description: string;
  file: string;
  downloadPath: string;
};

const raw: Omit<Edition, "downloadPath">[] = [
  { title: "Porn Blocker DE 3.6", tag: "Flagship · Deutsch", hue: 220, description: "Beschreibung folgt.", file: "porn-blocker-de-3.6" },
  { title: "Porn Blocker EN 1.6", tag: "Flagship · English", hue: 200, description: "Description coming soon.", file: "porn-blocker-en-1.6" },
  { title: "Porn Blocker DE 3.6 Lite", tag: "Lite · Deutsch", hue: 180, description: "Beschreibung folgt.", file: "porn-blocker-de-3.6-lite" },
  { title: "Porn Blocker EN 1.6 Lite", tag: "Lite · English", hue: 160, description: "Description coming soon.", file: "porn-blocker-en-1.6-lite" },
  { title: "Porn Blocker PV Beta 0.6", tag: "Preview · Deutsch", hue: 280, description: "Beschreibung folgt.", file: "porn-blocker-pv-beta-0.6" },
  { title: "Porn Blocker EN PV Beta 0.6", tag: "Preview · English", hue: 300, description: "Description coming soon.", file: "porn-blocker-en-pv-beta-0.6" },
  { title: "Porn Blocker 3.6 Debian DE", tag: "Debian · Deutsch", hue: 20, description: "Beschreibung folgt.", file: "porn-blocker-3.6-debian-de" },
  { title: "Porn Blocker 1.6 Debian EN", tag: "Debian · English", hue: 40, description: "Description coming soon.", file: "porn-blocker-1.6-debian-en" },
  { title: "Porn Blocker Turbo EN", tag: "Turbo · English", hue: 340, description: "Description coming soon.", file: "porn-blocker-turbo-en" },
  { title: "Porn Blocker Turbo DE", tag: "Turbo · Deutsch", hue: 0, description: "Beschreibung folgt.", file: "porn-blocker-turbo-de" },
];

export const editions: Edition[] = raw.map((e) => ({
  ...e,
  downloadPath: `/downloads/${e.file}.zip`,
}));
