import os

upload_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\upload.html'

def update_upload():
    with open(upload_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Summary Display
    display_old = """                                    <h3 class="font-bold text-xl text-gray-900" x-text="title || 'Summary Ready!'"></h3>
                                </div>
                                <div class="text-sm text-gray-700 leading-relaxed font-medium whitespace-pre-line" x-text="summary"></div>
                            </div>"""
    
    display_new = """                                    <h3 class="font-bold text-xl text-gray-900 flex-1" x-text="title || 'Summary Ready!'"></h3>
                                    <template x-if="currentDocId">
                                        <a :href="'/summarize/download/' + currentDocId + '/'" class="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl text-sm font-bold transition-all shadow-md">
                                            <i data-lucide="download" class="w-4 h-4"></i>
                                            Download PDF
                                        </a>
                                    </template>
                                </div>
                                <div class="text-sm text-gray-700 leading-relaxed font-medium whitespace-pre-line" x-text="summary"></div>
                            </div>"""

    if display_old in content:
        content = content.replace(display_old, display_new)
    
    # 2. Add currentDocId to Alpine state
    state_old = "summary: '',"
    state_new = "summary: '', currentDocId: null,"
    if state_old in content:
        content = content.replace(state_old, state_new)
    
    # 3. Update handleSubmit to set currentDocId
    submit_old = "this.summary = individualSummaries + \"🔄 --- Batch Synthesis ---\\n\\n\" + batchData.combined_summary;"
    submit_new = "this.summary = individualSummaries + \"🔄 --- Batch Synthesis ---\\n\\n\" + batchData.combined_summary; this.currentDocId = null; // Batch download not supported yet"
    if submit_old in content:
        content = content.replace(submit_old, submit_new)

    submit_single_old = "// For single files, just show the single summary as before"
    submit_single_new = "// For single files, just show the single summary as before\n                        this.currentDocId = processedDocIds[0];"
    if submit_single_old in content:
        content = content.replace(submit_single_old, submit_single_new)

    # 4. Update viewSummary to set currentDocId
    view_old = "this.summary = item.summary;"
    view_new = "this.summary = item.summary; this.currentDocId = item.id;"
    if view_old in content:
        content = content.replace(view_old, view_new)
    
    # Also handle the variant with replace
    view_variant_old = "this.summary = item.summary.replace(lines[0], '').trim();"
    view_variant_new = "this.summary = item.summary.replace(lines[0], '').trim(); this.currentDocId = item.id;"
    if view_variant_old in content:
        content = content.replace(view_variant_old, view_variant_new)

    with open(upload_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated upload.html UI for PDF downloads")

update_upload()
