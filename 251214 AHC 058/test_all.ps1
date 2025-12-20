# PowerShell 스크립트: 모든 테스트 케이스 실행
# 사용법: .\test_all.ps1

Write-Host "=== AtCoder AHC 056 Solver 테스트 ===" -ForegroundColor Cyan

# 솔버 컴파일
Write-Host "`n[1/3] 솔버 컴파일 중..." -ForegroundColor Yellow
g++ -std=c++17 -O3 solver.cpp -o solver.exe

if ($LASTEXITCODE -ne 0) {
    Write-Host "컴파일 실패!" -ForegroundColor Red
    exit 1
}
Write-Host "컴파일 완료!" -ForegroundColor Green

# 테스트 실행
Write-Host "`n[2/3] 테스트 케이스 실행 중..." -ForegroundColor Yellow

$inputFiles = Get-ChildItem -Path "in\*.txt" | Sort-Object Name
$totalScore = 0
$successCount = 0
$results = @()

foreach ($file in $inputFiles) {
    $caseName = $file.BaseName
    
    try {
        $output = Get-Content $file.FullName | ./solver.exe 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            $score = [long]$output
            $totalScore += $score
            $successCount++
            
            $results += [PSCustomObject]@{
                Case = $caseName
                Score = $score
                Status = "OK"
            }
            
            Write-Host ("[{0,3}/{1}] {2}: {3,20}" -f ($results.Count), $inputFiles.Count, $caseName, $score) -ForegroundColor White
        } else {
            $results += [PSCustomObject]@{
                Case = $caseName
                Score = 0
                Status = "FAILED"
            }
            Write-Host ("[{0,3}/{1}] {2}: FAILED" -f ($results.Count), $inputFiles.Count, $caseName) -ForegroundColor Red
        }
    } catch {
        $results += [PSCustomObject]@{
            Case = $caseName
            Score = 0
            Status = "ERROR"
        }
        Write-Host ("[{0,3}/{1}] {2}: ERROR" -f ($results.Count), $inputFiles.Count, $caseName) -ForegroundColor Red
    }
}

# 결과 저장
Write-Host "`n[3/3] 결과 저장 중..." -ForegroundColor Yellow

$results | Export-Csv -Path "results.csv" -NoTypeInformation -Encoding UTF8
$results | Format-Table -AutoSize | Out-File "results.txt" -Encoding UTF8

# 요약 출력
Write-Host "`n=== 테스트 결과 요약 ===" -ForegroundColor Cyan
Write-Host ("총점:   {0,20}" -f $totalScore) -ForegroundColor White
Write-Host ("평균:   {0,20:N2}" -f ($totalScore / $successCount)) -ForegroundColor White
Write-Host ("성공:   {0}/{1}" -f $successCount, $inputFiles.Count) -ForegroundColor White

Write-Host "`n결과가 results.txt 및 results.csv에 저장되었습니다." -ForegroundColor Green
