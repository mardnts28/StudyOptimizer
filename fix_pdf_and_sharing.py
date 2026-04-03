import os
import re

views_path = r'c:\Users\mary\Desktop\Study_Optimizer\Study_Optimizer\main\views.py'

def fix_views():
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Improve download_summary_pdf view
    pdf_view_old = """@login_required
def download_summary_pdf(request, doc_id):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    import io
    import re

    doc_obj = get_object_or_404(SummarizedDocument, id=doc_id, user=request.user)
    
    # We use io.BytesIO() as a buffer for the PDF
    buffer = io.BytesIO()
    
    # Create the SimpleDocTemplate with letter size
    final_pdf_doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    
    # Custom Title style
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#8C1007'),
        alignment=1, # Center
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    # Body style
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        fontName='Helvetica'
    )
    
    # We need to clean up any emojis or characters not in Helvetica
    # Simple regex to strip emojis for PDF compatibility
    clean_title = re.sub(r'[^\x00-\x7F]+', '', doc_obj.file_name)
    clean_summary = re.sub(r'[^\x00-\x7F]+', '', doc_obj.summary_text)

    elements = []
    
    # Title
    elements.append(Paragraph(f"Study Summary: {clean_title}", title_style))
    elements.append(Spacer(1, 12))
    
    # Summary Content (split into lines/paragraphs if needed, or just handle as Paragraph)
    # We replace newline characters with <br/> for Paragraph to handle line breaks
    formatted_summary = clean_summary.replace('\\n', '<br/>')
    elements.append(Paragraph(formatted_summary, body_style))
    
    # Build the PDF document
    final_pdf_doc.build(elements)
    
    # Get the value from the buffer and close it
    pdf = buffer.getvalue()
    buffer.close()
    
    # Prepare the response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Summary_{doc_id}.pdf"'
    response.write(pdf)
    
    AuditLog.objects.create(user=request.user, action="Downloaded PDF Summary", details=f"Document ID: {doc_id}")
    return response"""
    
    pdf_view_new = """@login_required
def download_summary_pdf(request, doc_id):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    import io
    import re

    try:
        doc_obj = get_object_or_404(SummarizedDocument, id=doc_id, user=request.user)
        buffer = io.BytesIO()
        final_pdf_doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#8C1007'), alignment=1, spaceAfter=20)
        body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14)
        
        # Strip all non-ASCII for ReportLab compatibility (basic fonts only)
        clean_title = re.sub(r'[^\x00-\x7F]+', '', str(doc_obj.file_name))
        clean_summary = re.sub(r'[^\x00-\x7F]+', '', str(doc_obj.summary_text))
        
        elements = [
            Paragraph(f"Study Summary: {clean_title}", title_style),
            Spacer(1, 12),
            Paragraph(clean_summary.replace('\\n', '<br/>'), body_style)
        ]
        
        final_pdf_doc.build(elements)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Summary_{doc_id}.pdf"'
        response['Content-Length'] = len(pdf_content)
        
        # Log action
        log = AuditLog(user=request.user, action="Downloaded PDF Summary")
        log.details = f"Document ID: {doc_id} | Name: {doc_obj.file_name}"
        log.save()
        
        return response
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"PDF Gen Error: {str(e)}")
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)"""

    # Replace PDF view
    content = content.replace(pdf_view_old, pdf_view_new)

    # 2. Update share_material view to handle FILES
    share_view_old = """@login_required
@require_POST
@ratelimit(key='ip', rate='10/m', block=True)
def share_material(request):
    try:
        import bleach
        data     = json.loads(request.body)
        title = bleach.clean(str(data.get('title', '')).strip())
        subject = bleach.clean(str(data.get('subject', '')).strip())
        preview = bleach.clean(str(data.get('preview', '')).strip())
        period = data.get('period', 'General')"""
        
    share_view_new = """@login_required
@require_POST
@ratelimit(key='ip', rate='10/m', block=True)
def share_material(request):
    try:
        import bleach
        # Standard form handling for multipart
        title   = bleach.clean(request.POST.get('title', '').strip())
        subject = bleach.clean(request.POST.get('subject', '').strip())
        preview = bleach.clean(request.POST.get('preview', '').strip())
        period  = request.POST.get('period', 'General')
        uploaded_file = request.FILES.get('file')"""
        
    content = content.replace(share_view_old, share_view_new)
    
    # 3. Update the item creation in share_material
    create_old = """        material = SharedMaterial.objects.create(
            author  = request.user,
            title   = title,
            subject = subject,
            content = preview,
            period  = period,
            emoji   = random.choice(['📄', '📝', '📚', '💡', '✍️'])
        )"""
        
    create_new = """        material = SharedMaterial.objects.create(
            author  = request.user,
            title   = title,
            subject = subject,
            content = preview,
            period  = period,
            file    = uploaded_file,
            emoji   = random.choice(['📄', '📝', '📚', '💡', '✍️'])
        )"""
    content = content.replace(create_old, create_new)

    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed PDF download and updated community sharing view for file uploads")

fix_views()
