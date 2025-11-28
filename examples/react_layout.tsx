/**
 * Responsive React Layout Component with Tailwind CSS
 *
 * Implements a modern application layout with:
 * - Collapsible sidebar
 * - Header with breadcrumbs
 * - Split pane (query input + results)
 * - Footer with status
 *
 * Based on Saisonxform Design System
 */

import React, { useState } from 'react';
import {
  Menu,
  X,
  Home,
  FileText,
  Settings,
  Users,
  ChevronRight,
  Search,
  Filter,
  Download,
  RefreshCw
} from 'lucide-react';

interface BreadcrumbItem {
  label: string;
  href: string;
}

interface LayoutProps {
  children?: React.ReactNode;
}

const MainLayout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const breadcrumbs: BreadcrumbItem[] = [
    { label: 'Home', href: '#' },
    { label: 'Dashboard', href: '#' },
    { label: 'Current Page', href: '#' },
  ];

  const sidebarItems = [
    { icon: Home, label: 'Dashboard', href: '#', badge: null },
    { icon: FileText, label: 'Documents', href: '#', badge: '12' },
    { icon: Users, label: 'Attendees', href: '#', badge: null },
    { icon: Settings, label: 'Settings', href: '#', badge: null },
  ];

  return (
    <div className="flex h-screen bg-neutral-50 overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`
          ${sidebarOpen ? 'w-64' : 'w-20'}
          bg-white border-r border-neutral-300
          transition-all duration-300 ease-in-out
          flex-shrink-0
          hidden md:flex md:flex-col
          shadow-sm
        `}
      >
        {/* Sidebar Header */}
        <div className="h-16 border-b border-neutral-300 flex items-center justify-between px-4">
          {sidebarOpen && (
            <h1 className="text-h4 font-semibold text-primary-700">
              Saisonxform
            </h1>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-md hover:bg-neutral-100 transition-colors"
            aria-label="Toggle sidebar"
          >
            <Menu className="w-5 h-5 text-neutral-700" />
          </button>
        </div>

        {/* Sidebar Navigation */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-2">
          {sidebarItems.map((item, index) => (
            <a
              key={index}
              href={item.href}
              className={`
                flex items-center gap-3 px-3 py-2.5 rounded-lg
                hover:bg-primary-50 hover:text-primary-700
                transition-all duration-200
                group relative
                ${!sidebarOpen && 'justify-center'}
              `}
            >
              <item.icon className="w-5 h-5 text-neutral-600 group-hover:text-primary-600" />
              {sidebarOpen && (
                <>
                  <span className="flex-1 text-body-sm font-medium text-neutral-700 group-hover:text-primary-700">
                    {item.label}
                  </span>
                  {item.badge && (
                    <span className="px-2 py-0.5 text-xs font-semibold bg-primary-100 text-primary-700 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </>
              )}
              {!sidebarOpen && item.badge && (
                <span className="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center text-xs font-semibold bg-primary-500 text-white rounded-full">
                  {item.badge}
                </span>
              )}
            </a>
          ))}
        </nav>

        {/* Sidebar Footer */}
        <div className="border-t border-neutral-300 p-4">
          <div className={`flex items-center gap-3 ${!sidebarOpen && 'justify-center'}`}>
            <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center">
              <span className="text-primary-700 font-semibold">JD</span>
            </div>
            {sidebarOpen && (
              <div className="flex-1">
                <p className="text-body-sm font-medium text-neutral-900">John Doe</p>
                <p className="text-caption text-neutral-600">john@example.com</p>
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* Mobile Sidebar Overlay */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 bg-black/50 z-40 md:hidden" onClick={() => setIsMobileMenuOpen(false)}>
          <aside
            className="absolute left-0 top-0 bottom-0 w-64 bg-white shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Mobile Sidebar Header */}
            <div className="h-16 border-b border-neutral-300 flex items-center justify-between px-4">
              <h1 className="text-h4 font-semibold text-primary-700">Saisonxform</h1>
              <button
                onClick={() => setIsMobileMenuOpen(false)}
                className="p-2 rounded-md hover:bg-neutral-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Mobile Navigation */}
            <nav className="p-4 space-y-2">
              {sidebarItems.map((item, index) => (
                <a
                  key={index}
                  href={item.href}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-primary-50 transition-colors"
                >
                  <item.icon className="w-5 h-5 text-neutral-600" />
                  <span className="flex-1 text-body-sm font-medium text-neutral-700">
                    {item.label}
                  </span>
                  {item.badge && (
                    <span className="px-2 py-0.5 text-xs font-semibold bg-primary-100 text-primary-700 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </a>
              ))}
            </nav>
          </aside>
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-white border-b border-neutral-300 flex items-center justify-between px-4 md:px-6 shadow-sm z-10">
          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(true)}
            className="p-2 rounded-md hover:bg-neutral-100 md:hidden"
          >
            <Menu className="w-5 h-5" />
          </button>

          {/* Breadcrumbs */}
          <nav className="flex items-center space-x-2 text-body-sm">
            {breadcrumbs.map((item, index) => (
              <React.Fragment key={index}>
                <a
                  href={item.href}
                  className={`
                    ${index === breadcrumbs.length - 1
                      ? 'text-neutral-900 font-medium'
                      : 'text-neutral-600 hover:text-primary-600'
                    }
                    transition-colors
                  `}
                >
                  {item.label}
                </a>
                {index < breadcrumbs.length - 1 && (
                  <ChevronRight className="w-4 h-4 text-neutral-400" />
                )}
              </React.Fragment>
            ))}
          </nav>

          {/* Header Actions */}
          <div className="flex items-center gap-2">
            <button className="p-2 rounded-md hover:bg-neutral-100 transition-colors">
              <Search className="w-5 h-5 text-neutral-600" />
            </button>
            <button className="p-2 rounded-md hover:bg-neutral-100 transition-colors">
              <RefreshCw className="w-5 h-5 text-neutral-600" />
            </button>
          </div>
        </header>

        {/* Content Area - Split Pane */}
        <main className="flex-1 flex flex-col lg:flex-row overflow-hidden">
          {/* Query Input Pane */}
          <div className="lg:w-1/2 border-b lg:border-b-0 lg:border-r border-neutral-300 bg-white overflow-y-auto">
            <div className="p-4 md:p-6 space-y-4">
              {/* Section Header */}
              <div className="flex items-center justify-between">
                <h2 className="text-h3 font-semibold text-neutral-900">Query Input</h2>
                <button className="p-2 rounded-md hover:bg-neutral-100 transition-colors">
                  <Filter className="w-5 h-5 text-neutral-600" />
                </button>
              </div>

              {/* Search Input */}
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search transactions..."
                  className="
                    w-full px-4 py-3 pr-10
                    border border-neutral-300 rounded-lg
                    focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
                    transition-all
                    text-body
                  "
                />
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400" />
              </div>

              {/* Filters */}
              <div className="space-y-3">
                <label className="block">
                  <span className="text-body-sm font-medium text-neutral-700 mb-1 block">
                    Date Range
                  </span>
                  <input
                    type="date"
                    className="
                      w-full px-4 py-2.5
                      border border-neutral-300 rounded-lg
                      focus:outline-none focus:ring-2 focus:ring-primary-500
                      text-body-sm
                    "
                  />
                </label>

                <label className="block">
                  <span className="text-body-sm font-medium text-neutral-700 mb-1 block">
                    Category
                  </span>
                  <select
                    className="
                      w-full px-4 py-2.5
                      border border-neutral-300 rounded-lg
                      focus:outline-none focus:ring-2 focus:ring-primary-500
                      text-body-sm
                    "
                  >
                    <option>All Categories</option>
                    <option>会議費 (Meeting Expenses)</option>
                    <option>接待費 (Entertainment)</option>
                  </select>
                </label>

                <label className="block">
                  <span className="text-body-sm font-medium text-neutral-700 mb-1 block">
                    Attendee Count
                  </span>
                  <div className="flex gap-2">
                    <input
                      type="number"
                      placeholder="Min"
                      className="
                        flex-1 px-4 py-2.5
                        border border-neutral-300 rounded-lg
                        focus:outline-none focus:ring-2 focus:ring-primary-500
                        text-body-sm
                      "
                    />
                    <input
                      type="number"
                      placeholder="Max"
                      className="
                        flex-1 px-4 py-2.5
                        border border-neutral-300 rounded-lg
                        focus:outline-none focus:ring-2 focus:ring-primary-500
                        text-body-sm
                      "
                    />
                  </div>
                </label>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2 pt-2">
                <button className="
                  flex-1 px-6 py-2.5
                  bg-primary-500 text-white
                  rounded-lg font-semibold
                  hover:bg-primary-600
                  transition-colors
                  shadow-sm hover:shadow-md
                ">
                  Apply Filters
                </button>
                <button className="
                  px-6 py-2.5
                  bg-neutral-100 text-neutral-700
                  rounded-lg font-semibold
                  hover:bg-neutral-200
                  transition-colors
                ">
                  Reset
                </button>
              </div>
            </div>
          </div>

          {/* Results Pane */}
          <div className="flex-1 bg-neutral-50 overflow-y-auto">
            <div className="p-4 md:p-6 space-y-4">
              {/* Section Header */}
              <div className="flex items-center justify-between">
                <h2 className="text-h3 font-semibold text-neutral-900">Results</h2>
                <button className="
                  flex items-center gap-2 px-4 py-2
                  bg-white border border-neutral-300 rounded-lg
                  hover:bg-neutral-50
                  transition-colors
                ">
                  <Download className="w-4 h-4" />
                  <span className="text-body-sm font-medium">Export</span>
                </button>
              </div>

              {/* Results Cards */}
              <div className="space-y-3">
                {[1, 2, 3, 4, 5].map((item) => (
                  <div
                    key={item}
                    className="
                      bg-white border border-neutral-300 rounded-lg p-4
                      hover:shadow-md transition-shadow
                      cursor-pointer
                    "
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="text-body font-semibold text-neutral-900">
                          Transaction #{item}
                        </h3>
                        <p className="text-body-sm text-neutral-600">
                          2025-11-{27 - item}
                        </p>
                      </div>
                      <span className="px-3 py-1 bg-success-light text-success-dark text-xs font-semibold rounded-full">
                        Processed
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-body-sm">
                      <span className="text-neutral-600">Amount:</span>
                      <span className="font-semibold text-neutral-900">
                        ¥{(5000 + item * 2000).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-body-sm mt-1">
                      <span className="text-neutral-600">Attendees:</span>
                      <span className="font-medium text-neutral-900">{2 + item}</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Empty State (conditionally shown) */}
              {false && (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <div className="w-16 h-16 bg-neutral-200 rounded-full flex items-center justify-center mb-4">
                    <Search className="w-8 h-8 text-neutral-400" />
                  </div>
                  <h3 className="text-h4 font-semibold text-neutral-900 mb-2">
                    No results found
                  </h3>
                  <p className="text-body-sm text-neutral-600">
                    Try adjusting your filters or search criteria
                  </p>
                </div>
              )}
            </div>
          </div>
        </main>

        {/* Footer / Status Bar */}
        <footer className="h-12 bg-white border-t border-neutral-300 flex items-center justify-between px-4 md:px-6 text-body-sm text-neutral-600 shadow-sm">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 bg-success rounded-full animate-pulse"></span>
              Connected
            </span>
            <span className="hidden md:inline">Last updated: 2 minutes ago</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden sm:inline">5 files processed</span>
            <span>847 total records</span>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default MainLayout;
