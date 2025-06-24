const vscode = require('vscode');
// THE FIX: Switch from 'spawn' to 'exec' for better command string control
const { exec } = require('child_process');
const path = require('path');

function activate(context) {
    console.log('Congratulations, your extension "pwl-tracker" is now active!');

    const onSaveHandler = vscode.workspace.onDidSaveTextDocument((document) => {
        if (document.uri.scheme !== 'file') {
            return;
        }

        const savedFilePath = document.fileName;
        const runnerScriptPath = path.join(__dirname, '..', '..', 'run_handler.bat');

        vscode.window.showInformationMessage(`File saved: ${savedFilePath}. Logging to PWL.`);

        // --- THE FINAL FIX ---
        // Construct the full command as a single string, with double quotes
        // around each path to handle spaces correctly. This is the most
        // robust way to execute commands with spaces on Windows.
        const command = `"${runnerScriptPath}" "${savedFilePath}"`;

        exec(command, (error, stdout, stderr) => {
            // The 'error' object is set if the command itself fails to run
            if (error) {
                console.error(`[PWL EXEC ERROR]: ${error.message}`);
                return;
            }
            // 'stderr' captures error output from within the running script
            if (stderr) {
                console.error(`[PWL Handler STDERR]: ${stderr}`);
            }
            // 'stdout' captures the successful output from our Python script
            console.log(`[PWL Handler STDOUT]: ${stdout}`);
        });
    });

    context.subscriptions.push(onSaveHandler);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}