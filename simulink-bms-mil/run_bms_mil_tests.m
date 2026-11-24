model = 'BMS_Protection_SoC';
load_system(model);

% Columns: Name, v_init, v_slope, i_init, i_slope, expected_fault_code
testCases = {
    'UnderVoltage_Entry', 2.80, 0.05, 0.0, 1.0, 2;  % Starts < 3.0V -> fault = 2
    'Normal_Window',      3.50, 0.02, 0.0, 0.5, 0;  % Stays in 3.0V-4.2V -> fault = 0
    'OverVoltage_Entry',  3.60, 0.20, 0.0, 1.5, 1;  % Crosses > 4.2V -> fault = 1
    'ZeroCurrent_Check',  3.70, 0.01, 0.0, 0.0, 0   % Zero current ramp -> SoC stays flat
    };

nTests = size(testCases, 1);
results = table('Size', [nTests, 6], ...
    'VariableTypes', {'string', 'double', 'double', 'double', 'double', 'logical'}, ...
    'VariableNames', {'TestCase', 'MinFault', 'MaxFault', 'StartSoC', 'EndSoC', 'Passed'});

for k = 1:nTests
    tcName   = testCases{k, 1};
    expFault = testCases{k, 6};

    assignin('base', 'v_init',  testCases{k, 2});
    assignin('base', 'v_slope', testCases{k, 3});
    assignin('base', 'i_init',  testCases{k, 4});
    assignin('base', 'i_slope', testCases{k, 5});

    simOut = sim(model, 'StopTime', '10');

    faultVec = [];
    socVec   = [];

    if isprop(simOut, 'logsout') && ~isempty(simOut.logsout)
        for idx = 1:simOut.logsout.numElements
            el = simOut.logsout.get(idx);
            sigName = lower(el.Name);
            if contains(sigName, 'fault') || contains(sigName, 'chart')
                faultVec = el.Values.Data(:);
            elseif contains(sigName, 'soc') || contains(sigName, 'integrator')
                socVec = el.Values.Data(:);
            end
        end
    end

    if isempty(faultVec) && isprop(simOut, 'yout') && ~isempty(simOut.yout)
        faultVec = simOut.yout{1}.Values.Data(:);
    end

    minF = NaN;
    maxF = NaN;
    passed = false;
    if ~isempty(faultVec)
        minF = min(faultVec);
        maxF = max(faultVec);
        passed = any(faultVec == expFault);
    end

    startSoC = NaN;
    endSoC   = NaN;
    if ~isempty(socVec)
        startSoC = socVec(1);
        endSoC   = socVec(end);
    end

    results(k, :) = {string(tcName), minF, maxF, startSoC, endSoC, passed};
    statusStr = "FAIL";
    if passed
        statusStr = "PASS";
    end
    fprintf('[%s] %s | fault=[%g, %g] | SoC=[%g -> %g]\n', ...
        statusStr, tcName, minF, maxF, startSoC, endSoC);
end

disp('=== BMS MIL Test Results ===');
disp(results);

save('bms_mil_results.mat', 'results', 'testCases');
writetable(results, 'bms_mil_results.csv');
disp('Saved bms_mil_results.mat and bms_mil_results.csv');