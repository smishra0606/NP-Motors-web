const { execSync } = require('child_process');

// 27th August 2026 se start karna hai
let currentDate = new Date('2026-08-27T10:00:00');
const endDate = new Date('2026-09-23T23:59:59'); // Aaj ki date

try {
    console.log("Checking for files in N.P. Motors project...");

    // Untracked aur modified files ko list karo
    const status = execSync('git ls-files --others --modified --exclude-standard').toString();
    const files = status.split('\n').filter(line => line.trim() !== '');

    if (files.length === 0) {
        console.log("Bhai, koi file nahi mili. 'git init', 'git add .' aur '.gitignore' check kar lo.");
        process.exit(0);
    }

    console.log(`Total ${files.length} files mili hain! Dark mode committing start kar rahe hain...`);

    let commitsToday = 0;

    // Kitne din hain calculate karo taaki files evenly distribute ho sakein
    const totalDays = Math.ceil((endDate - currentDate) / (1000 * 60 * 60 * 24));

    // Har din kitni files commit karni hain (taaki graph green rahe)
    let filesPerDay = Math.ceil(files.length / totalDays);
    if (filesPerDay < 1) filesPerDay = 1;

    // Target commits for the current day
    let targetCommitsForToday = filesPerDay + Math.floor(Math.random() * 3) - 1; // Thoda randomness
    if (targetCommitsForToday < 1) targetCommitsForToday = 1;

    files.forEach(file => {
        // Extra Safety Filter (Django/Python specific)
        if (
            file.includes('__pycache__/') ||
            file.includes('.venv/') ||
            file.includes('venv/') ||
            file.includes('db.sqlite3') ||
            file.includes('.env') ||
            file === 'auto-commit.js'
        ) return;

        console.log(`--> Committing: ${file}`);

        execSync(`git add "${file}"`);

        const dateStr = currentDate.toISOString();
        const fileName = file.split('/').pop();

        // Dynamic Commit Messages based on file type
        let commitMsg = `Developed feature/logic for ${fileName}`;
        if (fileName.endsWith('.html')) commitMsg = `Designed UI and template structure for ${fileName}`;
        else if (fileName.endsWith('.py')) commitMsg = `Implemented backend logic and routing in ${fileName}`;
        else if (fileName.endsWith('.css') || fileName.endsWith('.js')) commitMsg = `Added frontend assets and styling for ${fileName}`;

        execSync(`git commit -m "${commitMsg}"`, {
            env: {
                ...process.env,
                GIT_AUTHOR_DATE: dateStr,
                GIT_COMMITTER_DATE: dateStr
            }
        });

        commitsToday++;

        // Agar aaj ka target pura ho gaya, ya date future mein jaane wali hai
        if (commitsToday >= targetCommitsForToday) {
            currentDate.setDate(currentDate.getDate() + 1);

            // Time ko subah 10 se shaam 6 ke beech random rakho
            currentDate.setHours(10 + Math.floor(Math.random() * 8));

            commitsToday = 0;
            targetCommitsForToday = filesPerDay + Math.floor(Math.random() * 3) - 1;
            if (targetCommitsForToday < 1) targetCommitsForToday = 1;
        } else {
            // Din mein 1-2 ghante ka gap
            currentDate.setHours(currentDate.getHours() + Math.floor(Math.random() * 2) + 1);
        }

        // Safety check taaki future ki date me commit na ho jaye
        if (currentDate > endDate) {
            currentDate = new Date(endDate.getTime() - Math.floor(Math.random() * 1000 * 60 * 60 * 24));
        }
    });

    console.log("\n✅ Saare commits 27 Aug se distribute ho gaye! GitHub graph aag lagne ke liye ready hai.");

} catch (error) {
    console.error("❌ Kuch gadbad ho gayi:", error.message);
    if (error.stdout) console.error(error.stdout.toString());
}