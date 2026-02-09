import React from 'react';

export default function NewsThumbnails() {
  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <h1 className="text-3xl font-bold text-red-600 text-center mb-2 tracking-wider">
        📰 NEWS-STYLE THUMBNAILS
      </h1>
      <p className="text-gray-500 text-center mb-8 text-sm">
        Based on how real news outlets display Epstein documents
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">

        {/* Option A: Gmail Style */}
        <div className="bg-gray-800 rounded-xl overflow-hidden border-2 border-gray-700 hover:border-red-600 transition-colors">
          <div className="bg-gray-900 p-4 border-b border-gray-700">
            <h2 className="text-red-500 font-semibold">Option A: Gmail-Style</h2>
            <p className="text-gray-500 text-xs">Looks like an actual email client</p>
          </div>

          <div className="p-5 bg-black flex justify-center">
            <div className="w-72 bg-white rounded-lg overflow-hidden shadow-2xl">
              {/* Gmail header */}
              <div className="bg-blue-50 p-3 border-b border-gray-200 flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                  JE
                </div>
                <div>
                  <div className="text-sm font-semibold text-gray-800">Jeffrey Epstein</div>
                  <div className="text-xs text-gray-500">to Martha Stewart</div>
                  <div className="text-xs text-gray-400">Apr 15, 2012</div>
                </div>
              </div>
              {/* Email body */}
              <div className="p-4 text-xs text-gray-800 leading-relaxed">
                Martha,<br/><br/>
                Looking forward to <span className="bg-yellow-200 px-1">the party at my Hamptons estate</span> next weekend. The guest list is confirmed.<br/><br/>
                <span className="bg-yellow-200 px-1">Please keep this between us.</span>
              </div>
              {/* Caption */}
              <div className="bg-gray-900 text-gray-400 px-4 py-2 text-xs">
                📄 DOJ Release · Document #4521
              </div>
            </div>
          </div>

          <div className="p-4 text-gray-400 text-xs">
            Mimics email client with avatar, sender info, highlighted text, DOJ caption.
          </div>
        </div>

        {/* Option B: DOJ Redacted */}
        <div className="bg-gray-800 rounded-xl overflow-hidden border-2 border-gray-700 hover:border-red-600 transition-colors">
          <div className="bg-gray-900 p-4 border-b border-gray-700">
            <h2 className="text-red-500 font-semibold">Option B: DOJ Redacted</h2>
            <p className="text-gray-500 text-xs">Official FBI/DOJ with redactions</p>
          </div>

          <div className="p-5 bg-black flex justify-center">
            <div className="w-72 bg-white rounded-lg overflow-hidden shadow-2xl">
              {/* DOJ header */}
              <div className="bg-indigo-900 p-3 flex items-center gap-3">
                <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center text-indigo-900 font-bold text-xs">
                  DOJ
                </div>
                <div>
                  <div className="text-white text-sm font-semibold">Department of Justice</div>
                  <div className="text-indigo-300 text-xs">Declassified Document</div>
                </div>
              </div>
              {/* Document body */}
              <div className="p-4 text-xs text-gray-700 font-mono leading-loose">
                <span className="text-gray-500">FROM:</span> J. EPSTEIN<br/>
                <span className="text-gray-500">TO:</span> M. STEWART<br/>
                <span className="text-gray-500">DATE:</span> <span className="bg-black text-black px-4">████</span> 2012<br/><br/>
                Re: Hamptons party<br/><br/>
                Guest list includes <span className="bg-black text-black px-8">████████</span><br/>
                and several <span className="bg-black text-black px-6">██████</span>
              </div>
              {/* Doc ID */}
              <div className="bg-gray-100 px-4 py-2 text-xs text-gray-500 font-mono border-t">
                DOC ID: DOJ-EPS-2026-04521
              </div>
              {/* Caption */}
              <div className="bg-gray-900 text-gray-400 px-4 py-2 text-xs">
                📄 Released Jan 2026 · FOIA
              </div>
            </div>
          </div>

          <div className="p-4 text-gray-400 text-xs">
            Official DOJ look with black redaction bars and document ID.
          </div>
        </div>

        {/* Option C: Simple Clean */}
        <div className="bg-gray-800 rounded-xl overflow-hidden border-2 border-gray-700 hover:border-red-600 transition-colors">
          <div className="bg-gray-900 p-4 border-b border-gray-700">
            <h2 className="text-red-500 font-semibold">Option C: Simple & Clean</h2>
            <p className="text-gray-500 text-xs">Minimal, easy to read</p>
          </div>

          <div className="p-5 bg-black flex justify-center">
            <div className="w-72 bg-white rounded-lg overflow-hidden shadow-2xl">
              {/* Simple header */}
              <div className="p-4 border-b border-gray-200">
                <div className="flex text-xs mb-1">
                  <span className="text-gray-500 w-12">From:</span>
                  <span className="text-gray-800 font-medium">Jeffrey Epstein</span>
                </div>
                <div className="flex text-xs mb-1">
                  <span className="text-gray-500 w-12">To:</span>
                  <span className="text-gray-800 font-medium">Martha Stewart</span>
                </div>
                <div className="flex text-xs mb-1">
                  <span className="text-gray-500 w-12">Date:</span>
                  <span className="text-gray-800 font-medium">April 15, 2012</span>
                </div>
                <div className="flex text-xs">
                  <span className="text-gray-500 w-12">Re:</span>
                  <span className="text-gray-800 font-medium">Hamptons Party</span>
                </div>
              </div>
              {/* Body */}
              <div className="p-4 text-xs text-gray-800 leading-relaxed">
                Martha,<br/><br/>
                Looking forward to <span className="bg-yellow-200 px-1">the party at my estate</span> next weekend.<br/><br/>
                <span className="bg-yellow-200 px-1">Keep this between us.</span>
              </div>
              {/* Red caption */}
              <div className="bg-red-600 text-white px-4 py-2 text-xs flex justify-between">
                <span>DOJ Document Release</span>
                <span className="opacity-70">#4521</span>
              </div>
            </div>
          </div>

          <div className="p-4 text-gray-400 text-xs">
            Plain white background, minimal fields, yellow highlights, red caption.
          </div>
        </div>
      </div>
    </div>
  );
}
