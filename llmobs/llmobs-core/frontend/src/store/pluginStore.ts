import { create } from 'zustand'

interface Plugin {
  id: string
  name: string
  url: string
  enabled: boolean
}

interface PluginStore {
  plugins: Plugin[]
  addPlugin: (plugin: Plugin) => void
  removePlugin: (id: string) => void
  togglePlugin: (id: string) => void
}

export const usePluginStore = create<PluginStore>((set) => ({
  plugins: [],
  addPlugin: (plugin) =>
    set((state) => ({ plugins: [...state.plugins, plugin] })),
  removePlugin: (id) =>
    set((state) => ({
      plugins: state.plugins.filter((p) => p.id !== id),
    })),
  togglePlugin: (id) =>
    set((state) => ({
      plugins: state.plugins.map((p) =>
        p.id === id ? { ...p, enabled: !p.enabled } : p
      ),
    })),
}))
