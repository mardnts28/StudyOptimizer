import os
import re

collaborate_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\templates\main\collaborate.html'

def update_collaborate_ui():
    with open(collaborate_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add file input to Share Dialog
    dialog_old = """                    <div>
                        <label class="block font-semibold text-sm mb-1">Summary Content / Preview</label>
                        <textarea x-model="shareForm.preview" placeholder="Paste your summary here to share with classmates..." rows="5" class="w-full border-2 border-gray-200 rounded-lg p-3 text-sm resize-none focus:outline-none focus:border-red-300 transition-colors"></textarea>
                    </div>"""
    
    dialog_new = """                    <div>
                        <label class="block font-semibold text-sm mb-1">Summary Content / Preview</label>
                        <textarea x-model="shareForm.preview" placeholder="Paste your summary here to share with classmates..." rows="5" class="w-full border-2 border-gray-200 rounded-lg p-3 text-sm resize-none focus:outline-none focus:border-red-300 transition-colors"></textarea>
                    </div>
                    <div class="p-4 bg-red-50 border-2 border-dashed border-red-200 rounded-xl">
                        <label class="block font-bold text-xs text-red-700 uppercase tracking-widest mb-2">Upload File (Optional)</label>
                        <input type="file" @change="shareForm.file = $event.target.files[0]" 
                               class="w-full text-xs text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-bold file:bg-red-100 file:text-red-700 hover:file:bg-red-200 transition-all">
                        <p class="text-[10px] text-gray-400 mt-2 font-medium">Supported: .pdf, .docx, .pptx, .jpg, .png</p>
                    </div>"""
    
    if dialog_old in content:
        content = content.replace(dialog_old, dialog_new)

    # 2. Update Summary Card to show download button
    card_old = """                                    <button class="ml-auto flex items-center gap-1.5 text-sm font-medium text-gray-500 hover:text-green-600 transition-colors">
                                        <i data-lucide="thumbs-up" class="w-4 h-4"></i>
                                        Helpful
                                    </button>"""
    
    card_new = """                                    <template x-if="summary.file_url">
                                        <a :href="summary.file_url" target="_blank" class="ml-auto flex items-center gap-1.5 text-xs font-bold text-green-700 bg-green-50 px-3 py-1.5 rounded-lg border border-green-100 hover:bg-green-100 transition-all">
                                            <i data-lucide="download" class="w-3.5 h-3.5"></i>
                                            Download File
                                        </a>
                                    </template>
                                    <button x-show="!summary.file_url" class="ml-auto flex items-center gap-1.5 text-sm font-medium text-gray-500 hover:text-green-600 transition-colors">
                                        <i data-lucide="thumbs-up" class="w-4 h-4"></i>
                                        Helpful
                                    </button>"""
    
    if card_old in content:
        content = content.replace(card_old, card_new)

    # 3. Update handleShare JS to use FormData
    js_old = """                async handleShare() {
                    try {
                        const response = await fetch('/collaborate/share/', {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': '{{ csrf_token }}',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(this.shareForm)
                        });"""
    
    js_new = """                async handleShare() {
                    try {
                        const formData = new FormData();
                        formData.append('title', this.shareForm.title);
                        formData.append('subject', this.shareForm.subject);
                        formData.append('preview', this.shareForm.preview);
                        formData.append('period', this.shareForm.period);
                        if (this.shareForm.file) {
                            formData.append('file', this.shareForm.file);
                        }

                        const response = await fetch('/collaborate/share/', {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': '{{ csrf_token }}'
                                // Note: Fetch automatically sets the correct multipart boundary for FormData
                            },
                            body: formData
                        });"""
    
    if js_old in content:
        content = content.replace(js_old, js_new)
    
    # 3.5. Update state
    content = content.replace("shareForm: { title: '', subject: '', period: 'General', preview: '' },", 
                              "shareForm: { title: '', subject: '', period: 'General', preview: '', file: null },")

    with open(collaborate_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated collaborate.html UI with file upload support in sharing dialog")

update_collaborate_ui()
