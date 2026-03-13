# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. **"Method Not Allowed" Error**

**Problem**: Getting "Method Not Allowed" when trying to access the ask page.

**Solution**: 
- The `/ask` route now supports both GET and POST methods
- Make sure you're accessing the page with a GET request first
- The form should submit with a POST request

**Check**: Verify that `app/routes.py` has:
```python
@main_blueprint.route('/ask', methods=['GET', 'POST'])
```

### 2. **Translation Not Working**

**Problem**: Questions and answers are not being translated to the selected language.

**Possible Causes**:
- Google Translate API is not accessible
- Language codes are incorrect
- Translation service is rate-limited

**Solutions**:
1. **Check Internet Connection**: Ensure you have internet access
2. **Verify Language Codes**: Check that language codes match the supported list
3. **Test Translation API**: Use the test script to verify translation endpoints
4. **Check Logs**: Look at `app.log` for translation errors

**Test Translation**:
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "target_lang": "hi"}'
```

### 3. **AI Model Not Loading**

**Problem**: Getting "AI model is not available" error.

**Possible Causes**:
- Insufficient RAM (need 4GB+)
- Transformers library not installed
- Model download failed

**Solutions**:
1. **Check RAM**: Ensure you have at least 4GB available
2. **Reinstall Dependencies**: 
   ```bash
   pip uninstall transformers torch
   pip install transformers torch
   ```
3. **Use Smaller Model**: The system will automatically fallback to lighter models
4. **Check Logs**: Look for model loading errors in `app.log`

### 4. **Context Files Not Found**

**Problem**: "No study material available" error.

**Possible Causes**:
- Context files are missing from the `data/` directory
- File permissions are incorrect
- File paths are wrong

**Solutions**:
1. **Check File Structure**: Ensure `data/test_context.txt` exists
2. **Verify Permissions**: Make sure files are readable
3. **Check File Paths**: Verify paths in `SUBJECT_CONTEXTS` are correct
4. **Create Test Files**: Use the provided test context file

**File Structure Should Be**:
```
data/
├── test_context.txt          # Test content for all subjects
├── ncert_math_class9.txt    # Math content (optional)
├── ncert_science_class9.txt # Science content (optional)
└── ...
```

### 5. **Form Submission Issues**

**Problem**: Form is not submitting or showing errors.

**Possible Causes**:
- Missing required fields
- Form action URL is incorrect
- JavaScript errors

**Solutions**:
1. **Check Required Fields**: Ensure all required fields are filled
2. **Verify Form Action**: Form should submit to `/ask`
3. **Check Browser Console**: Look for JavaScript errors
4. **Validate Input**: Ensure question text is not empty

**Form Requirements**:
- `subject`: Must be selected
- `lang`: Must be selected (or auto-detect)
- `question`: Must not be empty

### 6. **Language Detection Not Working**

**Problem**: Auto-language detection is not working.

**Possible Causes**:
- Text is too short (need at least 3 characters)
- Language detection service is down
- Unsupported language

**Solutions**:
1. **Check Text Length**: Ensure question has at least 3 characters
2. **Manual Selection**: Manually select language if auto-detect fails
3. **Test Detection API**: Use the test script to verify
4. **Check Supported Languages**: Verify language is in the supported list

### 7. **Performance Issues**

**Problem**: Application is slow or unresponsive.

**Possible Causes**:
- Large context files
- Slow AI model inference
- Translation delays

**Solutions**:
1. **Optimize Context Files**: Keep files under 1MB each
2. **Use Smaller Models**: The system automatically selects appropriate models
3. **Enable Caching**: Check if caching is enabled in config
4. **Monitor Resources**: Check CPU and memory usage

### 8. **Quiz System Issues**

**Problem**: Quiz questions are not loading or submitting.

**Possible Causes**:
- Excel files are missing or corrupted
- File naming convention is incorrect
- Required columns are missing

**Solutions**:
1. **Check Excel Files**: Ensure quiz files exist in the correct format
2. **Verify File Names**: Use format `class{class}{subject}{difficulty}.xlsx`
3. **Check Columns**: Ensure these columns exist:
   - `question`
   - `option1`, `option2`, `option3`, `option4`
   - `answer`
4. **Test with Sample Data**: Create a simple test quiz file

## 🔍 **Debugging Steps**

### 1. **Check Application Logs**
```bash
tail -f app.log
```

### 2. **Test Individual Components**
```bash
python test_app.py
```

### 3. **Verify Dependencies**
```bash
pip list | grep -E "(flask|transformers|torch|googletrans)"
```

### 4. **Check File Permissions**
```bash
ls -la data/
ls -la app/
```

### 5. **Test API Endpoints**
```bash
# Test home page
curl http://localhost:5000/

# Test ask page
curl http://localhost:5000/ask

# Test translation
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Test", "source_lang": "en", "target_lang": "hi"}'
```

## 🚀 **Quick Fixes**

### **If Nothing Works**:
1. **Restart the Application**:
   ```bash
   # Stop the current instance
   Ctrl+C
   
   # Start again
   python app.py
   ```

2. **Clear Cache**:
   ```bash
   # Remove any cached files
   rm -rf __pycache__/
   rm -rf app/__pycache__/
   ```

3. **Reinstall Dependencies**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

4. **Check Python Version**:
   ```bash
   python --version  # Should be 3.8+
   ```

## 📞 **Getting Help**

If you're still experiencing issues:

1. **Check the logs** in `app.log`
2. **Run the test script** with `python test_app.py`
3. **Verify your setup** matches the requirements
4. **Check the GitHub issues** for similar problems
5. **Create a detailed bug report** with:
   - Error messages
   - Steps to reproduce
   - System information
   - Log files

## 🎯 **Prevention Tips**

1. **Regular Updates**: Keep dependencies updated
2. **Backup Data**: Regularly backup your context and quiz files
3. **Monitor Logs**: Check logs regularly for warnings
4. **Test Changes**: Test new features before deploying
5. **Resource Monitoring**: Monitor system resources during operation

---

**Remember**: Most issues can be resolved by checking the logs and following the debugging steps above!

