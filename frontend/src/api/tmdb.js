// Image URL helpers only. All TMDB API calls go through the backend,
// so no API key is shipped in the browser bundle.
export const IMAGE_BASE = 'https://image.tmdb.org/t/p';
export const posterUrl = (path, size = 'w500') =>
  path ? `${IMAGE_BASE}/${size}${path}` : null;
export const backdropUrl = (path, size = 'w1280') =>
  path ? `${IMAGE_BASE}/${size}${path}` : null;
