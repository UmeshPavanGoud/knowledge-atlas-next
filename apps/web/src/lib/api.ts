export const API = import.meta.env.VITE_API_URL || ''

export async function request<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${API}${path}`, { signal, headers: { Accept: 'application/json' } })
  if (!response.ok) {
    const detail = await response.text().catch(() => '')
    throw new Error(`Atlas API ${response.status}: ${detail || response.statusText}`)
  }
  return response.json() as Promise<T>
}
