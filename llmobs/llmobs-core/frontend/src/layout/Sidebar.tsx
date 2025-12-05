'use client'

import Link from 'next/link'
import { usePluginStore } from '@/store/pluginStore'

export function Sidebar() {
  const { plugins } = usePluginStore()

  return (
    <div className="w-64 bg-gray-900 text-white">
      <div className="p-6">
        <h1 className="text-2xl font-bold">LLMObs</h1>
      </div>
      <nav className="mt-6">
        <Link
          href="/"
          className="block px-6 py-3 hover:bg-gray-800 transition-colors"
        >
          Dashboard
        </Link>
        <Link
          href="/plugins"
          className="block px-6 py-3 hover:bg-gray-800 transition-colors"
        >
          Plugins
        </Link>
        <Link
          href="/settings"
          className="block px-6 py-3 hover:bg-gray-800 transition-colors"
        >
          Settings
        </Link>
        
        {plugins.length > 0 && (
          <div className="mt-8 px-6">
            <h3 className="text-xs uppercase text-gray-400 font-semibold mb-2">
              Active Plugins
            </h3>
            {plugins.map((plugin) => (
              <Link
                key={plugin.id}
                href={`/plugins/${plugin.id}`}
                className="block py-2 hover:text-blue-400 transition-colors"
              >
                {plugin.name}
              </Link>
            ))}
          </div>
        )}
      </nav>
    </div>
  )
}
