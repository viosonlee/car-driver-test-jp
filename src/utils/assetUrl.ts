export const resolveAssetUrl = (url?: string) => {
  if (!url) return '';
  if (/^(?:https?:|data:|blob:)/i.test(url)) return url;
  return `${import.meta.env.BASE_URL}${url.replace(/^\/+/, '')}`;
};
