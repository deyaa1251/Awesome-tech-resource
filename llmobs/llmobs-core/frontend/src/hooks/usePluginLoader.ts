import { useEffect, useState } from 'react'
import axios from 'axios'

interface PluginMetadata {
  id: string
  name: string
  remoteEntry: string
  scope: string
  module: string
}

export function usePluginLoader() {
  const [plugins, setPlugins] = useState<PluginMetadata[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPlugins()
  }, [])

  const loadPlugins = async () => {
    try {
      const response = await axios.get('/api/plugins')
      const pluginList = response.data

      const loadedPlugins = await Promise.all(
        pluginList.map(async (plugin: PluginMetadata) => {
          try {
            // Dynamically load the remote module
            await loadRemoteModule(plugin.remoteEntry, plugin.scope)
            return plugin
          } catch (error) {
            console.error(`Failed to load plugin ${plugin.name}:`, error)
            return null
          }
        })
      )

      setPlugins(loadedPlugins.filter(Boolean) as PluginMetadata[])
    } catch (error) {
      console.error('Failed to fetch plugins:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadRemoteModule = async (url: string, scope: string) => {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = url
      script.type = 'text/javascript'
      script.async = true

      script.onload = () => {
        // @ts-ignore
        const container = window[scope]
        if (!container) {
          reject(new Error(`Container ${scope} not found`))
          return
        }

        // @ts-ignore
        container.init(__webpack_share_scopes__.default)
        resolve(container)
      }

      script.onerror = () => {
        reject(new Error(`Failed to load script: ${url}`))
      }

      document.head.appendChild(script)
    })
  }

  return { plugins, loading, reload: loadPlugins }
}
