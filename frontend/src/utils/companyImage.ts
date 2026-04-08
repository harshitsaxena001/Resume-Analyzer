const palette = [
  ["#1F2322", "#48C6B4"],
  ["#F4DCCB", "#EAF4F1"],
  ["#F9EBE0", "#48C6B4"],
  ["#1F2322", "#F4D03F"],
  ["#EAF4F1", "#1F2322"],
  ["#FDFBF6", "#A7DCCF"],
];

const getInitials = (companyName: string) => {
  const words = companyName.trim().split(/\s+/).filter(Boolean);
  if (words.length === 0) return "SS";
  if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
  return `${words[0][0]}${words[1][0]}`.toUpperCase();
};

const hashCompanyName = (companyName: string) => {
  let hash = 0;
  for (let index = 0; index < companyName.length; index += 1) {
    hash = (hash * 31 + companyName.charCodeAt(index)) >>> 0;
  }
  return hash;
};

export const createCompanyAvatarDataUri = (companyName: string, size = 240) => {
  const initials = getInitials(companyName);
  const [startColor, endColor] =
    palette[hashCompanyName(companyName) % palette.length];
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
      <defs>
        <linearGradient id="gradient" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="${startColor}" />
          <stop offset="100%" stop-color="${endColor}" />
        </linearGradient>
      </defs>
      <rect width="${size}" height="${size}" rx="${size * 0.28}" fill="url(#gradient)" />
      <circle cx="${size * 0.77}" cy="${size * 0.24}" r="${size * 0.13}" fill="rgba(255,255,255,0.18)" />
      <circle cx="${size * 0.2}" cy="${size * 0.76}" r="${size * 0.18}" fill="rgba(255,255,255,0.12)" />
      <path d="M${size * 0.18} ${size * 0.53} C${size * 0.32} ${size * 0.35}, ${size * 0.48} ${size * 0.28}, ${size * 0.62} ${size * 0.37} C${size * 0.75} ${size * 0.45}, ${size * 0.8} ${size * 0.62}, ${size * 0.68} ${size * 0.74}" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="${size * 0.035}" stroke-linecap="round" />
      <text x="50%" y="53%" text-anchor="middle" dominant-baseline="middle" fill="#FFFFFF" font-family="Arial, Helvetica, sans-serif" font-size="${size * 0.33}" font-weight="700" letter-spacing="${size * 0.01}">${initials}</text>
    </svg>
  `;
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg.trim())}`;
};

export const createCompanyBannerDataUri = (
  companyName: string,
  width = 1400,
  height = 420,
) => {
  const [startColor, endColor] =
    palette[(hashCompanyName(companyName) + 2) % palette.length];
  const accent =
    palette[(hashCompanyName(companyName) + 4) % palette.length][1];
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
      <defs>
        <linearGradient id="bannerGradient" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="${startColor}" />
          <stop offset="55%" stop-color="${endColor}" />
          <stop offset="100%" stop-color="#1F2322" />
        </linearGradient>
      </defs>
      <rect width="${width}" height="${height}" rx="32" fill="url(#bannerGradient)" />
      <circle cx="${width * 0.8}" cy="${height * 0.22}" r="${height * 0.22}" fill="rgba(255,255,255,0.08)" />
      <circle cx="${width * 0.1}" cy="${height * 0.72}" r="${height * 0.18}" fill="rgba(255,255,255,0.05)" />
      <path d="M0 ${height * 0.76} C${width * 0.16} ${height * 0.58}, ${width * 0.26} ${height * 0.92}, ${width * 0.44} ${height * 0.7} C${width * 0.58} ${height * 0.54}, ${width * 0.73} ${height * 0.84}, ${width} ${height * 0.58} L${width} ${height} L0 ${height} Z" fill="rgba(255,255,255,0.08)" />
      <path d="M${width * 0.1} ${height * 0.62} H${width * 0.9}" stroke="rgba(255,255,255,0.2)" stroke-width="3" stroke-dasharray="18 18" />
      <text x="6%" y="22%" fill="rgba(255,255,255,0.78)" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="700">${companyName}</text>
      <text x="6%" y="30%" fill="rgba(255,255,255,0.62)" font-family="Arial, Helvetica, sans-serif" font-size="18">Clean hiring, thoughtfully presented</text>
      <rect x="6%" y="40%" width="140" height="8" rx="4" fill="${accent}" />
    </svg>
  `;
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg.trim())}`;
};
